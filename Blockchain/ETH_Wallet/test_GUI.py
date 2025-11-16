import tkinter as tk


class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("主界面")

        # 创建按钮用于跳转到新界面
        self.button = tk.Button(master, text="点击跳转", command=self.open_new_window)
        self.button.pack(pady=20)

    def open_new_window(self):
        new_window = tk.Toplevel(self.master)
        new_window.title("设置短密码")
        window_width = 400
        window_height = 300
        screen_width = new_window.winfo_screenwidth()
        screen_height = new_window.winfo_screenheight()
        x_pos = (screen_width - window_width) // 2
        y_pos = (screen_height - window_height) // 2
        new_window.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")
        label = tk.Label(new_window, text="")
        label.pack(pady=10)
        self.set_shortKey_button = tk.Button(new_window, text="新建短密码", font=("黑体", 10), command=self.set_key,
                                             bg='#F8EFEF')
        self.set_shortKey_button.grid(row=1, column=1, sticky="SE", padx=20, pady=20)
        self.change_shortKey_button = tk.Button(new_window, text="修改短密码", font=("黑体", 10), command=self.set_key,
                                                bg='#F8EFEF')
        self.change_shortKey_button.grid(row=1, column=2, sticky="SE", padx=20, pady=20)
        close_button = tk.Button(new_window, text="关闭窗口", command=new_window.destroy)
        close_button.pack(pady=20)

    def set_key(self):
        return


def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
