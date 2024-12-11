import sys
if sys.platform != 'win32':
    import termios
    import tty

def getch(debug=False):
    """Cross-platform character input"""
    if sys.platform == 'win32':
        import msvcrt
        first = msvcrt.getch()
        if debug:
            print("\nDEBUG getch() - First byte:", first)
            
        if first in [b'\xe0', b'\x00']:  # Special keys
            second = msvcrt.getch()
            if debug:
                print("DEBUG getch() - Second byte:", second)
                
            # Windows arrow keys mapping
            if second == b'H':    # Up arrow
                result = '\x1b[A'
            elif second == b'P':  # Down arrow
                result = '\x1b[B'
            elif second == b'K':  # Left arrow
                result = '\x1b[D'
            elif second == b'M':  # Right arrow
                result = '\x1b[C'
            else:
                result = 'x'  # Default for unmapped special keys
                
            if debug:
                print("DEBUG getch() - Mapped to:", repr(result))  # Use repr to see escape sequences
                
            return result
            
        return first.decode('utf-8', errors='replace')
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch