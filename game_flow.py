





def get_controller_input(queue):

    while True:
        event = get_gamepad()[0]
        queue.put(event)
        # print(event.code)

def draw_screen(queue):
    try:
        event = queue.get(block=False)
    except Empty:
        event = None
    else:
        print(event.code)






if __name__ == '__main__':



    events = Queue()

    # draw_screen(events)
    gamepad_listener = threading.Thread(target=get_controller_input, args=(events,))
    # drawer = threading.Thread(target=draw_screen, args=(events,))

    gamepad_listener.start()

    while 1:
        draw_screen(events)

