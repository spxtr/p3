class Stats:
    def __init__(self):
        self.total_frames = 0
        self.skipped_frames = 0
        self.thinking_time = 0

    def __str__(self):
        if not self.total_frames:
            return ''
        frac_thinking = self.thinking_time * 1000 / self.total_frames
        return '\n'.join(
            ['Total Frames: {}'.format(self.total_frames),
             'Skipped: {}'.format(self.skipped_frames),
             'Average Thinking Time (ms): {:.6f}'.format(frac_thinking)])

    def add_frames(self, frames):
        self.total_frames += frames
        if frames > 1:
            self.skipped_frames += frames - 1

    def add_thinking_time(self, thinking_time):
        self.thinking_time += thinking_time
