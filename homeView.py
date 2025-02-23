# Minhas Kamal (minhaskamal024@gmail.com)
# 13 Mar 24

import tkinter as tk

class HomeView:
    create_new_movement_option = "Create new movement"
    create_new_patient_option = "Create new patient"
    perform_movement_option = "Perform movement"

    @classmethod
    def show(cls, view_frame: tk.Frame, operation_option: tk.StringVar) -> None:
        view_frame.name = cls.__name__

        tk.Label(
            view_frame,
            text="Select operation").pack(
                padx=10,
                pady=(10, 40))
        tk.Radiobutton(
            view_frame,
            text=cls.create_new_movement_option,
            value=cls.create_new_movement_option,
            variable=operation_option).pack(
                padx=10,
                pady=(5, 5))
        tk.Radiobutton(
            view_frame,
            text=cls.create_new_patient_option,
            value=cls.create_new_patient_option,
            variable=operation_option).pack(
                padx=10,
                pady=(5, 5))
        tk.Radiobutton(
            view_frame,
            text=cls.perform_movement_option,
            value=cls.perform_movement_option,
            variable=operation_option).pack(
                padx=10,
                pady=(5, 50))

        return

# test
if __name__ == "__main__":
    ui = tk.Tk()
    ui.option_add("*Font", ('Arial', 12))
    ui.option_add("*Background", "#fff")
    view_frame = tk.Frame(ui)
    view_frame.pack(fill="both")
    operation_option = tk.StringVar(view_frame, "0")
    HomeView.show(view_frame, operation_option)
    ui.mainloop()
    print(operation_option.get())

