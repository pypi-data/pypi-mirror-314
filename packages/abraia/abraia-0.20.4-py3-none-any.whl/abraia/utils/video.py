import cv2


class Video:
    def __init__(self, src=0, output=None):
        self.out = None
        self.quit = False
        self.win_name = ''
        self.cap = cv2.VideoCapture(src)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.frame_rate = self.fps
        if output:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.out = cv2.VideoWriter(output, fourcc, self.fps, (self.width, self.height))

    def __iter__(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret is False or frame is None or self.quit:
                break
            yield cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.cap.release()
        if self.out:
            self.out.release()
        if self.win_name:
            cv2.destroyWindow(self.win_name)
            cv2.waitKey(1)

    def write(self, frame):
        self.out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    
    def show(self, frame):
        if not self.win_name:
            self.win_name = 'Video'
            cv2.namedWindow(self.win_name, cv2.WINDOW_GUI_NORMAL)
        cv2.imshow(self.win_name, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        ch = 0xFF & cv2.waitKey(int(self.fps))
        if (ch == 27 or ch == ord('q')) or cv2.getWindowProperty(self.win_name, cv2.WND_PROP_VISIBLE) < 1:
            self.quit = True
