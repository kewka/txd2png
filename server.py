'''
txd2png-server.
This is a small TCP server to convert TXD to PNG files.

Request:
[txd_size] - Header with TXD file size. Size: {config.HEADER_SIZE} bytes (Max: {config.MAX_FILE_SIZE}).
[txd_data] - The contents of the TXD file. Size: [txd_size] bytes.

Response:
[png_count] - Header with the number of PNG files. Size: {config.HEADER_SIZE} byte.
[png_file] - {
    [png_size] - Header with PNG file size. Size: {config.HEADER_SIZE} bytes.
    [png_content] - The contents of the PNG file. Size: [png_size] bytes.
}
'''

import socket
import threading
import uuid
import os
import shutil
import config
from script import convert


def handle_request(client: socket.socket):
    # Generate file id.
    id = str(uuid.uuid1())

    # Path to working directory,
    working_dir = os.path.join(config.TEMP_DIR, id)

    # Path to TXD file.
    txd_path = os.path.join(working_dir, id + '.txd')

    # Set the socket timeout.
    client.settimeout(config.SOCKET_TIMEOUT_SECONDS)
    
    # Create working directory.
    os.mkdir(working_dir)

    print('ID: %s' % id)

    def clean():
        try:
            # Remove working directory.
            shutil.rmtree(working_dir)
            # Close connection.
            client.close()
            print('[%s] Cleaning complete.' % id)
        except Exception as e:
            print('[%s] Cleaning error: %s' % (id, str(e)))

    try:
        # Get header bytes.
        header = client.recv(config.HEADER_SIZE)
        # Get file size from header.
        filesize = int.from_bytes(header, config.HEADER_BYTEORDER)

        # Check file size.
        if filesize > config.MAX_FILE_SIZE:
            return clean()

        # Number of bytes read.
        bytes_read = 0

        with open(txd_path, 'wb') as txd:
            while bytes_read < filesize:
                remaining = filesize - bytes_read
                chunk = client.recv(config.BUFFER_SIZE if remaining >
                                    config.BUFFER_SIZE else remaining)

                bytes_read += len(chunk)
                txd.write(chunk)

        png_files = convert(txd_path, working_dir)
        png_count = len(png_files)

        if png_count:
            # Send [png_count].
            client.send(png_count.to_bytes(config.HEADER_SIZE, config.HEADER_BYTEORDER))

            for png_file in png_files:
                png_path = os.path.join(working_dir, png_file + '.png')
                png_size = os.path.getsize(png_path)

                # Send [png_size].
                client.send(png_size.to_bytes(config.HEADER_SIZE, config.HEADER_BYTEORDER))

                with open(png_path, 'rb') as png:
                    # Send [png_content].
                    while True:
                        chunk = png.read(config.BUFFER_SIZE)

                        if not chunk:
                            break

                        client.send(chunk)

        return clean()
    except socket.timeout:
        print('[%s] Socket timeout error' % id)
        return clean()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(config.SERVER_ADDRESS)
    server.listen()
    print('txd2png-server running on %s:%d' % config.SERVER_ADDRESS)

    while True:
        client, addr = server.accept()
        print('New client')
        threading.Thread(target=handle_request, args=(client,)).start()

    server.close()


if __name__ == '__main__':
    main()
