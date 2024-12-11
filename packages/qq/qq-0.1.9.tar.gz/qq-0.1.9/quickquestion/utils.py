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
                print("DEBUG getch() - Mapped to:", repr(result))
                
            return result
            
        return first.decode('utf-8', errors='replace')
    else:
        # Unix systems (macOS, Linux)
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            first = sys.stdin.read(1)
            if debug:
                print("\nDEBUG getch() - First byte:", repr(first))

            if first == '\x1b':  # Escape sequence
                # Read potential escape sequence
                second = sys.stdin.read(1)
                if debug:
                    print("DEBUG getch() - Second byte:", repr(second))
                
                if second == '[':
                    third = sys.stdin.read(1)
                    if debug:
                        print("DEBUG getch() - Third byte:", repr(third))
                    
                    # Map arrow keys
                    result = '\x1b[' + third
                    
                    if debug:
                        print("DEBUG getch() - Mapped to:", repr(result))
                        
                    return result
                
                # Handle non-arrow escape sequences
                return first + second
            
            return first
            
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)