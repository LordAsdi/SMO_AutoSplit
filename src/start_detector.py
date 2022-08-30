import numpy as np
import cv2


class StartDetector:
    def __init__(self):
        self.start_vals = []
        self.btn_center = [0, 0, 0]
        self.prev_btn_center = [0, 0, 0]
        self.avgs = 0, 0, 0, 0

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
            self.prev_btn_center = self.btn_center

            frame_crop = frame[280:340, 470:570]
            frame_bw = cv2.cvtColor(frame_crop, cv2.COLOR_RGB2GRAY)
            img_blur = cv2.GaussianBlur(frame_bw, (3, 3), 0)
            sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5)
            sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5)

            h_x, h_w, h_y, h_h, h_o = (10, 76, 9, 2, 41)
            v_x, v_w, v_y, v_h, v_o = (4, 2, 17, 35, 80)

            _, sobelx_th = cv2.threshold(sobelx, 64, 255, cv2.THRESH_BINARY)
            _, sobely_th = cv2.threshold(sobely, 64, 255, cv2.THRESH_BINARY)

            crop1 = sobely_th[h_y:h_y + h_h, h_x:h_x + h_w]
            avg1 = crop1.mean(axis=0).mean(axis=0)

            crop2 = sobely_th[h_y:h_y + h_h, h_x:h_x + h_w]
            avg2 = crop2.mean(axis=0).mean(axis=0)

            crop3 = sobelx_th[v_y:v_y + v_h, v_x:v_x + v_w]
            avg3 = crop3.mean(axis=0).mean(axis=0)

            crop4 = sobelx_th[v_y:v_y + v_h, v_x:v_x + v_w]
            avg4 = crop4.mean(axis=0).mean(axis=0)

            self.avgs = avg1, avg2, avg3, avg4

            sobelx_bgr = cv2.cvtColor(np.float32(sobelx_th), cv2.COLOR_GRAY2BGR)
            sobely_bgr = cv2.cvtColor(np.float32(sobely_th), cv2.COLOR_GRAY2BGR)
            cv2.rectangle(sobely_bgr, (h_x, h_y), (h_x + h_w, h_y + h_h), (255, 0, 0), 1)
            cv2.rectangle(sobely_bgr, (h_x, h_y + h_o), (h_x + h_w, h_y + h_o + h_h), (255, 0, 0), 1)
            cv2.rectangle(sobelx_bgr, (v_x, v_y), (v_x + v_w, v_y + v_h), (255, 0, 0), 1)
            cv2.rectangle(sobelx_bgr, (v_x + v_o, v_y), (v_x + v_o + v_w, v_y + v_h), (255, 0, 0), 1)

            self.btn_center = frame[300:300 + 26, 484:484 + 6].mean(axis=0).mean(axis=0)

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
        avg1, avg2, avg3, avg4 = self.avgs
        if avg1 > 128 and avg2 > 128 and avg3 > 128 and avg4 > 128 and \
                45 < self.prev_btn_center[0] < 65 and self.prev_btn_center[2] < 75 and self.prev_btn_center[1] < 70 and \
                45 < self.btn_center[0] < 65 and self.btn_center[2] > 70 and self.btn_center[1] > 70:
            return True

        return False
