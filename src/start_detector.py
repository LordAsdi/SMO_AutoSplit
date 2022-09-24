import time
import numpy as np
import cv2


class StartDetector:
    def __init__(self):
        self.start_vals = []

        self.ok_btn = False
        self.prev_ok_btn = False
        self.ok_btn_time = 0
        self.date_time_border = False

        # Parameters
        self.lower_hue = 170
        self.upper_hue = 190
        self.lower_sat = 245
        self.lower_val = 200

    def update(self, frame, start_button=False, date_time_ok=False):
        if start_button:
            frame_bw = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            text_crop = frame_bw[179:179 + 53, 93:93 + 30]
            ret, text_crop_th = cv2.threshold(text_crop, 128, 255, cv2.THRESH_BINARY)
            _, contours, hirearchy = cv2.findContours(255 - text_crop_th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Detect cappy
            cappy_crop = frame[209:210, 74:75]
            cappy_crop_hsv = cv2.cvtColor(cappy_crop, cv2.COLOR_RGB2HSV)
            cappy_pixel_hsv = cappy_crop_hsv[0][0]

            if cappy_pixel_hsv[0] <= 90:
                cappy_pixel_hsv[0] += 180

            cappy = False
            if self.lower_hue < cappy_pixel_hsv[0] < self.upper_hue \
                    and cappy_pixel_hsv[1] > self.lower_sat and cappy_pixel_hsv[2] > self.lower_val:
                cappy = True

            tmp = frame[179:179 + 53, 93:93 + 30]

            # Detect text
            if len(contours) > 0:
                boxes = []
                for c in contours:
                    (x, y, w, h) = cv2.boundingRect(c)
                    boxes.append([x, y, x + w, y + h])

                boxes = np.asarray(boxes)
                left, top = np.min(boxes, axis=0)[:2]
                right, bottom = np.max(boxes, axis=0)[2:]

                cv2.rectangle(tmp, (left, top), (right, bottom), (255, 0, 0), 1)

                self.start_vals.append((cappy, top, bottom))
            else:
                self.start_vals.append((False, 0, 0))

            while len(self.start_vals) > 10:
                self.start_vals.pop(0)

        if date_time_ok:
            self.prev_ok_btn = self.ok_btn

            # Detect ok button
            frame_crop = frame[280:340, 501:601]
            frame_bw = cv2.cvtColor(frame_crop, cv2.COLOR_RGB2GRAY)
            img_blur = cv2.GaussianBlur(frame_bw, (3, 3), 0)
            sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5)

            h_x, h_w, h_y, h_h, h_o = (10, 40, 9, 2, 41)

            _, sobely_th = cv2.threshold(sobely, 64, 255, cv2.THRESH_BINARY)

            crop_top = sobely_th[h_y:h_y + h_h, h_x:h_x + h_w]
            ok_btn_top = crop_top.mean(axis=0).mean(axis=0)

            # To check if button is highlighted
            crop_top_rgb_avg = frame_crop[h_y + 2:h_y + 2 + h_h, h_x:h_x + h_w].mean(axis=1).mean(axis=0)

            crop_bot = sobely_th[h_y:h_y + h_h, h_x:h_x + h_w]
            ok_btn_bot = crop_bot.mean(axis=0).mean(axis=0)

            if ok_btn_top > 127 and ok_btn_bot > 127 and \
                    crop_top_rgb_avg[0] * 1.1 < crop_top_rgb_avg[1] and crop_top_rgb_avg[0] * 1.1 < crop_top_rgb_avg[2]:
                self.ok_btn = True
            else:
                self.ok_btn = False

            if not self.ok_btn and self.prev_ok_btn:
                self.ok_btn_time = time.time()

            # Draw rects for debugging
            # sobely_bgr = cv2.cvtColor(np.float32(sobely_th), cv2.COLOR_GRAY2BGR)
            # cv2.rectangle(sobely_bgr, (h_x, h_y), (h_x + h_w, h_y + h_h), (255, 0, 0), 1)
            # cv2.rectangle(sobely_bgr, (h_x, h_y + h_o), (h_x + h_w, h_y + h_o + h_h), (255, 0, 0), 1)
            # cv2.imshow("a", cv2.cvtColor(cv2.resize(sobely_bgr, (0, 0), fx=3, fy=3, interpolation=cv2.INTER_NEAREST),
            #                              cv2.COLOR_RGB2BGR))

            # Detect date time border
            frame_crop = frame[223:283, 400:500]
            frame_bw = cv2.cvtColor(frame_crop, cv2.COLOR_RGB2GRAY)
            img_blur = cv2.GaussianBlur(frame_bw, (3, 3), 0)
            sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5)

            h_x, h_w, h_y, h_h, h_o = (10, 40, 4, 2, 50)

            _, sobely_th = cv2.threshold(sobely, 64, 255, cv2.THRESH_BINARY)

            crop_top = sobely_th[h_y:h_y + h_h, h_x:h_x + h_w]
            date_time_border_top = crop_top.mean(axis=0).mean(axis=0)

            crop_bot = sobely_th[h_y:h_y + h_h, h_x:h_x + h_w]
            date_time_border_bot = crop_bot.mean(axis=0).mean(axis=0)

            if date_time_border_top > 127 and date_time_border_bot > 127:
                self.date_time_border = True
            else:
                self.date_time_border = False

            # Draw rects for debugging
            # sobely_bgr = cv2.cvtColor(np.float32(sobely_th), cv2.COLOR_GRAY2BGR)
            # cv2.rectangle(sobely_bgr, (h_x, h_y), (h_x + h_w, h_y + h_h), (255, 0, 0), 1)
            # cv2.rectangle(sobely_bgr, (h_x, h_y + h_o), (h_x + h_w, h_y + h_o + h_h), (255, 0, 0), 1)
            # cv2.imshow("b", cv2.cvtColor(cv2.resize(sobely_bgr, (0, 0), fx=3, fy=3, interpolation=cv2.INTER_NEAREST),
            #                              cv2.COLOR_RGB2BGR))
            # if cv2.waitKey(1) == 23:
            #     return

    def check_start_button(self):
        if len(self.start_vals) < 10:
            return False

        start_vals_rev = [x for x in reversed(self.start_vals)]
        i = 0
        prev_val = (False, 0, 0)

        for val in start_vals_rev:
            cappy, top, bottom = val
            prev_cappy, prev_top, prev_bottom = prev_val

            if not cappy:
                return False

            if i == 1 and (prev_top == top or prev_bottom == bottom):
                return False

            if i > 1:
                if val != prev_val or top == 0 or bottom == 53:
                    return False

            prev_val = val
            i += 1

        return True

    def check_date_time_ok(self):
        if self.date_time_border and time.time() < self.ok_btn_time + 0.06:
            return True

        return False
