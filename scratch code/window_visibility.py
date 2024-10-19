import win32gui
import psutil

import win32con

# Function to get the window rectangle (position and size)
def get_window_rect(hwnd):
    '''
    :arg hwnd:
    :fun: this function returns the upper left corner pixel of the window
        and the bottom right. For example (200, 300, 1200, 1400). (200,
        300) would be the top left corner and (1200, 1400) would be the 
        bottom right
    '''
    return win32gui.GetWindowRect(hwnd)


def filter_gui(processes):
    pass




def get_visibility_map(processes):
    # Get Rects

    # Calculate Coverage
    # enum

    # Return Dict
    pass

def get_window_rects(processess):
    pass

def get_window_coverage(window, allWindows):
    pass


# Function to check if a window is covered by any other windows
def is_window_covered(target_hwnd):
    target_rect = get_window_rect(target_hwnd)
    
    # Enumerate all windows and check their positions
    def enum_windows_callback(hwnd, lParam):
        if hwnd == target_hwnd:  # Skip the target window itself
            return True

        # Check if the other window is visible
        if win32gui.IsWindowVisible(hwnd):
            other_rect = get_window_rect(hwnd)
            # If the other window overlaps the target window, it is covered
            if rects_overlap(target_rect, other_rect):
                lParam.append(hwnd)
        return True

    # List to store windows that overlap with the target window
    overlapping_windows = []
    # Lists all windows from top to bottom
    win32gui.EnumWindows(enum_windows_callback, overlapping_windows)

    # IDEA: Since it is top to bottom, we could build a coverage mask. The next window checks if it is personally 
    # visible through the mask and then it adds to the mask after its personal check.

    # If there are any overlapping windows, the target window is covered
    return len(overlapping_windows) > 0


# Function to check if two rectangles overlap
def rects_overlap(rect1, rect2): 
    '''
    
    '''
    # Unpack the rectangles (left, top, right, bottom)
    left1, top1, right1, bottom1 = rect1
    left2, top2, right2, bottom2 = rect2
    
    # Check if the two rectangles overlap
    return not (right1 <= left2 or right2 <= left1 or bottom1 <= top2 or bottom2 <= top1)


if __name__ == "__main__":
    # Test with a specific window title
    window_title = "Untitled - Notepad"  # Replace with the title of the window you want to check
    target_hwnd = win32gui.FindWindow(None, window_title)

    if target_hwnd == 0:
        print(f"Window '{window_title}' not found.")
    else:
        if is_window_covered(target_hwnd):
            print(f"Window '{window_title}' is covered by another window.")
        else:
            print(f"Window '{window_title}' is not covered.")



for process in psutil.process_iter():
    print(process.pid())