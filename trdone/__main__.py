from application import Application

if __name__ == '__main__':
    import sys

    app = Application()
    app.parse_arguments(sys.argv[1:])
    app.run()
