# SHA-256 Hash Algorithm Implementation

A complete SHA-256 hash algorithm implementation project, including a manually implemented algorithm core, a graphical interface, and command-line testing tools.

## Project Introduction

This project implements the SHA-256 (Secure Hash Algorithm 256-bit) hash algorithm, providing two implementation methods:

- **Manual Implementation**: Implementing the complete SHA-256 algorithm from scratch.

- **Library Function Implementation**: Using the Java standard library `MessageDigest` as a reference implementation.

The project includes both command-line tools and a graphical interface, supporting hash calculations for text and files.

## Features

- Complete manual implementation of the SHA-256 algorithm

- Supports text string hash calculation

- Supports text file (.txt) hash calculation

- Supports image file (.jpg, .png) hash calculation

- Graphical user interface (GUI)

- Command-line testing tool

- Result verification function (comparing manual implementation with library function implementation)

## Project Structure

``` sha256_hash/

├── SHA256.java # Core implementation of the SHA-256 algorithm (manual implementation)

├── SHA256_.java # SHA-256 library function implementation (for verification)

├── GUI.java # Graphical interface program

├── Test.java # Command-line testing program

└── sha256_hash.iml # IntelliJ IDEA project configuration file

```

## Core Class Description

### SHA256.java is a manually implemented core class for the SHA-256 algorithm, containing:

- **Message Preprocessing**: Padding to ensure the message length is a multiple of 512 bits.

- **Message Blocking**: Dividing the message into 512-bit blocks.

- **Message Expansion**: Expanding 16 words into 64 words.

- **64 Rounds of Iteration**: Executing the SHA-256 compression function.

- **Auxiliary Functions**: Bitwise operations (XOR, AND, NOT), circular right shift, right shift, etc.

### SHA256_.java is an implementation of SHA-256 using the Java standard library `MessageDigest`, used to verify the correctness of the manually implemented version.

### GUI.java A graphical user interface program providing:

- Text input box (supports drag-and-drop file input)

- Hash result display (manual implementation and library function implementation)

- Verification function (comparing the results of the two implementations)

- Clear function

### Test.java A command-line testing program that supports looping string input and calculating hash values.

## Usage Methods

### Method 1: Graphical Interface (Recommended)

1. Compile the project:

```bash
javac sha256_hash/*.java

```

2. Run the GUI program:

```bash
java sha256_hash.GUI

```

3. Instructions:

- Enter the text to be hashed in the text box, or drag and drop the file directly into the text box.

- Supported file types:

- `.txt` text files

- `.jpg` image files

- `.png` image files

- Click the "Calculate" button to calculate the hash value.

- Click the "Verify" button to verify if the results of the two implementations are consistent.

- Click the "Clear" button to clear all content.

### Method 2: Command Line Tool

1. Compile the project:

```bash
javac sha256_hash/*.java

```

2. Run the test program:

```bash
java sha256_hash.Test

```

3. Usage instructions:

- The program will prompt you to enter a string

- After entering the string and pressing Enter, the program will display:

- Manually implemented SHA-256 result

- Result implemented by the library function

- Verify the result (whether it matches)

- The program will run in a loop, and you can continue to enter new strings

## Technical implementation details

### SHA-256 algorithm flow

1. **Message preprocessing**

- Convert the message to binary

- Add a '1' to the end of the message

- Fill with '0' until the length satisfies: `(length + 64) % 512 == 0`

- Add the binary representation of the original message length to the last 64 bits

2. **Message block division**

- Divide the preprocessed message into 512-bit blocks

- Each block is further divided into 16 32-bit words (w[0] to w[15])

3. **Message expansion**

- Expand the message Expanding 16 words to 64 words

- w[i] = w[i-16] + w[i-7] + σ₀(w[i-15]) + σ₁(w[i-2])

4. **Compression Function**

- Uses 8 initial hash values ​​(H₀ to H₇)

- Performs 64 rounds of iteration on each 512-bit block

- Uses the obfuscation constant K[i] and the expanded word w[i] in each round

5. **Final Hash Value**

- Sum the hash values ​​of all blocks

- Outputs a 256-bit (64 hexadecimal characters) hash value

## Notes

**Important Notes**:

1. **Character Encoding**: Due to inconsistent encoding methods, **it is not recommended to input Chinese characters**, otherwise the hash result may be inconsistent with the standard implementation.

2. **File Format**:

- Text files should use ASCII characters, avoiding non-ASCII characters.

- Image files only support `.jpg` and `.png` formats.

- Images will be converted to Base64 encoding before hash calculation.

3. **Performance**: Manual implementation is primarily for learning and understanding algorithm principles; its performance may be inferior to the standard library implementation.

4. **Verification**: It is recommended to use the "Verification" function to ensure the correctness of the manual implementation.

## Development Environment

- **Programming Language**: Java

- **Java Version**: Supports Java 8 and above.

## Algorithm Reference

The SHA-256 algorithm follows the FIPS 180-4 standard, and this implementation strictly adheres to the standard specifications.

## License

This project is for learning and research purposes only.