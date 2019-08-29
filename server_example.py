import os
import socket
import config

EXAMPLE_FILE = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'example/ballas3.txd'))


def server_example():
    # Get txd size.
    txd_size = os.path.getsize(EXAMPLE_FILE)
    # Create connection.
    connection = socket.create_connection(config.SERVER_ADDRESS)
    # Send txd size.
    connection.send(txd_size.to_bytes(config.HEADER_SIZE,
                                      config.HEADER_BYTEORDER))

    # Send txd data.
    with open(EXAMPLE_FILE, 'rb') as txd:
        while True:
            chunk = txd.read()

            if not chunk:
                break

            connection.send(chunk)

    # Read png count.
    png_count = int.from_bytes(connection.recv(
        config.HEADER_SIZE), config.HEADER_BYTEORDER)
    print('PNG count: %d' % png_count)

    for i in range(png_count):
        filename, _ = os.path.splitext(EXAMPLE_FILE)
        png_file = os.path.join(os.path.dirname(
            EXAMPLE_FILE), "%s_%d.png" % (filename, i))

        # Read png size.
        png_size = int.from_bytes(connection.recv(
            config.HEADER_SIZE), config.HEADER_BYTEORDER)
        print('PNG size: %d' % png_size)

        # Write png data to file.
        bytes_written = 0

        with open(png_file, 'wb') as png:
            while bytes_written < png_size:
                while True:
                    # Read png data.
                    png_data = connection.recv(
                        min(config.BUFFER_SIZE, png_size - bytes_written))

                    if not png_data:
                        break

                    bytes_written += png.write(png_data)

    connection.close()


if __name__ == '__main__':
    server_example()
