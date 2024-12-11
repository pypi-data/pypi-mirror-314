import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, CheckButtons, RectangleSelector
from matplotlib.gridspec import GridSpec
import random

from .._utils.helper import find_nex_smaller_wave

# State dictionary to manage the global variables locally
state = {
    'layer_id': 0,
    'normalize_flag': False
}

saved_plots = []  # To hold saved plot data (wave, spec, roi info, color)
saved_lines = []  # To hold the actual line objects for plotting
saved_rois = []  # To hold ROI rectangles for display


def normalize(spec):
    """Normalize the spectrum to the range 0-1 if needed."""
    spec_min, spec_max = spec.min(), spec.max()
    return np.clip((spec - spec_min) / (spec_max - spec_min), 0, 1) if spec_max > spec_min else spec


def plotter(dc):
    """
    Plotter function to explore the DataCube.

    :param dc: DataCube with beatuifull data
    """
    state['layer_id'] = 0  # Initialize layer ID

    # Initialize ROI coordinates
    roi_x_start, roi_x_end = 0, dc.cube.shape[2]
    roi_y_start, roi_y_end = 0, dc.cube.shape[1]
    
    def update_plot(_=None):
        """Update the main plot with current state."""
        layer_index = state['layer_id']
        layer = dc.cube[layer_index]
        imshow.set_data(layer)
        imshow.set_clim(vmin=layer.min(), vmax=layer.max())
        layer_id = dc.wavelengths[state["layer_id"]]
        notation = dc.notation or ""
        ax[0].set_title(f'Image @{notation}{layer_id}')

        # Update the vertical line to the current wavelength layer
        line.set_xdata([dc.wavelengths[state['layer_id']]])

        # Update ROI mean plot
        update_roi_mean()

        # Update saved plots without re-adding lines
        for i, sp in enumerate(saved_plots):
            saved_spec = sp['spec']
            if state['normalize_flag']:
                saved_spec = normalize(saved_spec)
            saved_lines[i].set_data(sp['wave'], saved_spec)
            saved_lines[i].set_color(sp['color'])  # Use saved color

        fig.canvas.draw_idle()

    def save_plot(_):
        """Save the current spectrum data and ROI coordinates to saved_plots."""
        roi_data = dc.cube[:, roi_y_start:roi_y_end, roi_x_start:roi_x_end]
        mean_spec = np.mean(roi_data, axis=(1, 2))
        if state['normalize_flag']:
            mean_spec = normalize(mean_spec)

        # Generate a random color for this ROI and save it with the plot
        color = (random.random(), random.random(), random.random())  # Random RGB color
        saved_plots.append({
            'wave': dc.wavelengths,
            'spec': mean_spec,
            'roi': (roi_x_start, roi_x_end, roi_y_start, roi_y_end),  # Save ROI coordinates
            'color': color
        })

        # Plot with the specific color for the saved ROI
        saved_line, = ax[1].plot(saved_plots[-1]['wave'], saved_plots[-1]['spec'], color=color, alpha=0.4)
        saved_lines.append(saved_line)

        # Draw the rectangle on the image to represent the ROI and save it
        roi_rect = plt.Rectangle((roi_x_start, roi_y_start), roi_x_end - roi_x_start, roi_y_end - roi_y_start,
                                 linewidth=2, edgecolor=color, facecolor=color, alpha=0.4)
        ax[0].add_patch(roi_rect)
        saved_rois.append(roi_rect)  # Store the rectangle so we can manage it later

        update_plot()

    def remove_last_plot(_):
        """Remove the last saved plot and its corresponding ROI rectangle."""
        if saved_plots:
            saved_plots.pop()
            saved_lines.pop().remove()

            # Remove the corresponding ROI rectangle
            if saved_rois:
                roi_rect = saved_rois.pop()
                roi_rect.remove()

            update_plot()

    def toggle_normalization(_):
        state['normalize_flag'] = not state['normalize_flag']
        update_plot()

    def update_roi_mean():
        """Compute and plot the mean spectrum over the selected ROI."""
        roi_data = dc.cube[:, roi_y_start:roi_y_end, roi_x_start:roi_x_end]
        mean_spec = np.mean(roi_data, axis=(1, 2))
        if state['normalize_flag']:
            mean_spec = normalize(mean_spec)

        # Define range padding
        r = (mean_spec.max() - mean_spec.min()) * 0.1
        ax[1].set_ylim(0 if state['normalize_flag'] else mean_spec.min() - r,
                       1 if state['normalize_flag'] else mean_spec.max() + r)
        roi_line.set_data(dc.wavelengths, mean_spec)

    def on_roi_change(eclick, erelease):
        """Handle rectangle selector change to update ROI coordinates."""
        nonlocal roi_x_start, roi_x_end, roi_y_start, roi_y_end

        roi_x_start, roi_y_start = int(eclick.xdata), int(eclick.ydata)
        roi_x_end, roi_y_end = int(erelease.xdata), int(erelease.ydata)

        if roi_x_start - roi_x_end == 0:
            roi_x_end += 1
        if roi_y_start - roi_y_end == 0:
            roi_y_end += 1

        update_plot()

    def onclick_select(event):
        """Handle rectangle selector change to update ROI coordinates."""
        nonlocal roi_x_start, roi_x_end, roi_y_start, roi_y_end
        if event.inaxes == ax[0]:
            roi_x, roi_y = int(event.xdata), int(event.ydata)
            roi_x_start, roi_x_end = roi_x, roi_x + 1
            roi_y_start, roi_y_end = roi_y, roi_y + 1
            update_plot()
        elif event.inaxes == ax[1]:
            try:
                state['layer_id'] = np.where(dc.wavelengths == find_nex_smaller_wave(dc.wavelengths, int(event.xdata), 10))[0][0]
            except IndexError:
                return
            update_plot()

    # Create main figure and layout with GridSpec
    fig = plt.figure(figsize=(14, 8))
    gs = GridSpec(2, 2, width_ratios=[4, 4], height_ratios=[4, 1])

    # Main plotting area (image and spectrum)
    ax_image = fig.add_subplot(gs[0, 0])
    ax_spectrum = fig.add_subplot(gs[0, 1])
    ax_spectrum.set_title('Spectrum')
    ax = [ax_image, ax_spectrum]

    # Control panel for buttons and checkbox
    ax_control = fig.add_subplot(gs[1, :])
    ax_control.axis("off")

    # Set up the initial plots
    layer = dc.cube[0]
    imshow = ax[0].imshow(layer)
    spec = dc.cube[:, 0, 0]
    line = ax[1].axvline(x=state['layer_id'], color='lightgrey', linestyle='dashed')

    # ROI mean line
    roi_line, = ax[1].plot(dc.wavelengths, spec, label="ROI Mean")
    ax[1].set_xlabel(f'{dc.notation}')
    ax[1].set_ylabel('Counts')
    ax[1].set_xlim(dc.wavelengths.min(), dc.wavelengths.max())

    # Buttons and checkbox in the control panel
    ax_save = fig.add_axes([0.05, 0.1, 0.15, 0.075])
    btn_save = Button(ax_save, 'Save Plot')
    btn_save.on_clicked(save_plot)

    ax_remove = fig.add_axes([0.25, 0.1, 0.15, 0.075])
    btn_remove = Button(ax_remove, 'Remove Plot')
    btn_remove.on_clicked(remove_last_plot)

    ax_checkbox = fig.add_axes([0.45, 0.1, 0.15, 0.075])
    check = CheckButtons(ax_checkbox, ['Normalize Y (0-1)'], [False])
    check.on_clicked(toggle_normalization)

    # ROI selection
    #  _ = is nessasary, otherwise the roi selctor wouldn't wrok 
    _ = RectangleSelector(ax[0], on_roi_change, useblit=True, button=[1], minspanx=5, minspany=5, spancoords='pixels', interactive=True)
    fig.canvas.mpl_connect("button_press_event", onclick_select)

    update_plot()

    plt.tight_layout(rect=[0, 0, .95, 1])
    plt.show()
