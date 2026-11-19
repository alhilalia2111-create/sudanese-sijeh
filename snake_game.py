
# -*- coding: utf-8 -*-
"""
RX SIJEH | السيجة السودانية
RX COMPUTER TECHNOLOGY
Developed by: HEL Lalia

لعبة استراتيجية سودانية - لاعبان على جهاز واحد.
المكتبات المطلوبة: Tkinter (ضمن تثبيت Python المعتاد).
"""

import tkinter as tk
from tkinter import messagebox

SIZE = 5
CELL = 90
MARGIN = 35
CENTER = (2, 2)
PIECES = 12

BG = "#101827"
BLUE = "#1686D9"
GOLD = "#E9A23B"
WHITE = "#FFFFFF"
BOARD = "#D8B982"
LINE = "#75552E"


class RXSiege:

    def __init__(self, root):
        self.root = root
        self.root.title("RX SIJEH | السيجة السودانية")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.reset_data()
        self.create_interface()
        self.refresh()

    def reset_data(self):
        self.board = [[0] * SIZE for _ in range(SIZE)]
        self.remaining = {1: PIECES, 2: PIECES}
        self.captured = {1: 0, 2: 0}
        self.player = 1
        self.phase = "placement"
        self.selected = None
        self.placed = 0
        self.game_over = False

    def create_interface(self):
        tk.Label(
            self.root,
            text="RX SIJEH",
            font=("Arial", 27, "bold"),
            fg="#55B7FF", bg=BG
        ).pack(pady=(15, 2))

        tk.Label(
            self.root,
            text="السيجة السودانية | SUDANESE HERITAGE",
            font=("Arial", 13, "bold"),
            fg=WHITE, bg=BG
        ).pack()

        tk.Label(
            self.root,
            text="RX COMPUTER TECHNOLOGY",
            font=("Arial", 10, "bold"),
            fg="#AAB7C8", bg=BG
        ).pack(pady=5)

        self.status = tk.Label(
            self.root,
            font=("Arial", 12, "bold"),
            fg=WHITE, bg="#172338",
            padx=15, pady=12
        )
        self.status.pack(fill="x", padx=18, pady=10)

        self.canvas = tk.Canvas(
            self.root,
            width=SIZE * CELL + 2 * MARGIN,
            height=SIZE * CELL + 2 * MARGIN,
            bg=BOARD,
            highlightthickness=0
        )
        self.canvas.pack(padx=15, pady=5)
        self.canvas.bind("<Button-1>", self.click)

        self.score = tk.Label(
            self.root,
            font=("Arial", 11, "bold"),
            fg=WHITE, bg=BG
        )
        self.score.pack(pady=12)

        controls = tk.Frame(self.root, bg=BG)
        controls.pack(pady=8)

        tk.Button(
            controls,
            text="قواعد اللعبة",
            command=self.rules,
            font=("Arial", 10, "bold"),
            bg="#263B58", fg=WHITE,
            relief="flat", padx=15, pady=8
        ).pack(side="left", padx=5)

        tk.Button(
            controls,
            text="لعبة جديدة",
            command=self.new_game,
            font=("Arial", 10, "bold"),
            bg=BLUE, fg=WHITE,
            relief="flat", padx=15, pady=8
        ).pack(side="left", padx=5)

        tk.Label(
            self.root,
            text="Developed by HEL Lalia | RX Computer Technology",
            font=("Arial", 8),
            fg="#AAB7C8", bg=BG
        ).pack(pady=10)

    def position(self, r, c):
        return MARGIN + c * CELL, MARGIN + r * CELL

    def draw(self):
        self.canvas.delete("all")

        start = MARGIN
        end = MARGIN + (SIZE - 1) * CELL

        # رسم شبكة اللعب
        for i in range(SIZE):
            p = MARGIN + i * CELL
            self.canvas.create_line(
                p, start, p, end,
                fill=LINE, width=4
            )
            self.canvas.create_line(
                start, p, end, p,
                fill=LINE, width=4
            )

        # المركز المحجوز
        x, y = self.position(*CENTER)
        self.canvas.create_oval(
            x-19, y-19, x+19, y+19,
            fill="#B99A66", outline=LINE, width=2
        )
        self.canvas.create_text(
            x, y+30, text="المركز",
            fill="#60451F", font=("Arial", 8)
        )

        # رسم القطع
        for r in range(SIZE):
            for c in range(SIZE):
                if (r, c) == CENTER:
                    continue

                x, y = self.position(r, c)
                value = self.board[r][c]

                if value:
                    color = BLUE if value == 1 else GOLD
                    self.canvas.create_oval(
                        x-25, y-25, x+25, y+25,
                        fill=color, outline=WHITE, width=3
                    )
                    self.canvas.create_oval(
                        x-8, y-8, x+8, y+8,
                        fill=WHITE, outline=""
                    )
                else:
                    self.canvas.create_oval(
                        x-5, y-5, x+5, y+5,
                        fill=LINE, outline=""
                    )

                if self.selected == (r, c):
                    self.canvas.create_oval(
                        x-32, y-32, x+32, y+32,
                        outline="#F4D35E", width=4
                    )

    def refresh(self):
        self.draw()

        name = "الأزرق" if self.player == 1 else "الذهبي"
        color = BLUE if self.player == 1 else GOLD

        if self.game_over:
            text = "انتهت المباراة"
        elif self.phase == "placement":
            text = f"مرحلة توزيع القطع | دور اللاعب {name}"
        else:
            text = f"مرحلة الحركة | دور اللاعب {name}"

        self.status.config(text=text, fg=color)

        self.score.config(
            text=(
                f"الأزرق: متبقي {self.remaining[1]} | "
                f"أسر {self.captured[1]}       "
                f"الذهبي: متبقي {self.remaining[2]} | "
                f"أسر {self.captured[2]}"
            )
        )

    def click(self, event):
        if self.game_over:
            return

        c = round((event.x - MARGIN) / CELL)
        r = round((event.y - MARGIN) / CELL)

        if not (0 <= r < SIZE and 0 <= c < SIZE):
            return

        x, y = self.position(r, c)
        if abs(event.x-x) > CELL*.42 or abs(event.y-y) > CELL*.42:
            return

        if (r, c) == CENTER:
            return

        if self.phase == "placement":
            self.place(r, c)
        else:
            self.move(r, c)

    def place(self, r, c):
        if self.board[r][c] != 0:
            return

        self.board[r][c] = self.player
        self.remaining[self.player] -= 1
        self.placed += 1

        if self.remaining[1] == 0 and self.remaining[2] == 0:
            self.phase = "movement"
            self.player = 1
            self.placed = 0
            messagebox.showinfo(
                "RX SIJEH",
                "اكتمل توزيع القطع. بدأت مرحلة الحركة!"
            )
        else:
            needed = min(2, self.remaining[self.player] + self.placed)
            if self.placed >= needed:
                self.placed = 0
                self.player = 3 - self.player

        self.refresh()

    def move(self, r, c):
        if self.selected is None:
            if self.board[r][c] == self.player:
                self.selected = (r, c)
            self.refresh()
            return

        sr, sc = self.selected

        if (r, c) == (sr, sc):
            self.selected = None
            self.refresh()
            return

        if self.board[r][c] == self.player:
            self.selected = (r, c)
            self.refresh()
            return

        if self.board[r][c] != 0:
            self.selected = None
            self.refresh()
            return

        if abs(r-sr) + abs(c-sc) != 1:
            self.selected = None
            self.refresh()
            return

        self.board[r][c] = self.player
        self.board[sr][sc] = 0
        self.selected = None

        self.capture(r, c)

        winner = self.winner()
        if winner:
            self.end_game(winner)
            return

        self.player = 3 - self.player
        self.refresh()

    def capture(self, r, c):
        enemy = 3 - self.player
        captured_positions = []

        directions = [
            (1, 0), (-1, 0),
            (0, 1), (0, -1)
        ]

        for dr, dc in directions:
            r1, c1 = r+dr, c+dc
            r2, c2 = r+2*dr, c+2*dc

            if not (0 <= r2 < SIZE and 0 <= c2 < SIZE):
                continue

            if (
                self.board[r1][c1] == enemy
                and self.board[r2][c2] == self.player
            ):
                captured_positions.append((r1, c1))

        for rr, cc in captured_positions:
            self.board[rr][cc] = 0
            self.captured[self.player] += 1

    def legal_move(self, player):
        for r in range(SIZE):
            for c in range(SIZE):
                if self.board[r][c] != player:
                    continue

                for dr, dc in [
                    (1, 0), (-1, 0),
                    (0, 1), (0, -1)
                ]:
                    nr, nc = r+dr, c+dc

                    if not (0 <= nr < SIZE and 0 <= nc < SIZE):
                        continue

                    if (nr, nc) == CENTER:
                        continue

                    if self.board[nr][nc] == 0:
                        return True

        return False

    def winner(self):
        count = {
            p: sum(cell == p for row in self.board for cell in row)
            for p in (1, 2)
        }

        if count[1] == 0:
            return 2
        if count[2] == 0:
            return 1

        enemy = 3 - self.player
        if not self.legal_move(enemy):
            return self.player

        return None

    def end_game(self, winner):
        self.game_over = True
        self.refresh()

        name = "الأزرق" if winner == 1 else "الذهبي"

        messagebox.showinfo(
            "RX SIJEH",
            f"مبروك! اللاعب {name} هو الفائز!\n\n"
            "RX COMPUTER TECHNOLOGY"
        )

    def new_game(self):
        self.reset_data()
        self.refresh()

    def rules(self):
        messagebox.showinfo(
            "قواعد السيجة",
            "1. لكل لاعب 12 قطعة.\n"
            "2. توضع قطعتان في كل دور.\n"
            "3. المركز محجوز.\n"
            "4. بعد التوزيع تبدأ الحركة.\n"
            "5. تتحرك القطعة خانة واحدة أفقياً أو رأسياً.\n"
            "6. تحاصر قطعة الخصم بين قطعتين لك لتأسرها.\n"
            "7. الفائز من يزيل قطع خصمه أو يمنعه من الحركة.\n\n"
            "نسخة تعليمية مبسطة من اللعبة."
        )


if __name__ == "__main__":
    root = tk.Tk()
    game = RXSiege(root)
    root.mainloop()
