hello hackers, 
this is a basic python scripts for a reverse shell payload .....
And what it does is :

    Creates a TCP socket and connects to the attacker's IP/port
    Listens for commands from the attacker
    Executes received commands locally using subprocess.getoutput()
    Sends results back through the socket
    Exits when receiving "exit" command

To use this:

    Set up a listener on attacker machine:

    bash

    nc -lvnp 4444

    Run this script on target machine
    Commands sent to the listener will be executed on target

Security considerations

    No input validation - commands could execute arbitrary code
    Uses encrypted communication using AES-256-CFB
we do not promote any unethical use of this script so kindly hack ethically...
keep hacking bye bye....
