def doc(value):
    try:
        print(value.__doc__)
    except KeyError:
        return
if __name__ == '__main__':
    doc(slice)