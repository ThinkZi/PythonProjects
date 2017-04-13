
#This is not working yet ...
class Action():
    def view_command(self):
        list1.delete(0,END)
        for row in database.view():
            list1.insert(END,row)

    def search_command(self):
        list1.delete(0,END)
        for row in database.search(title_text.get(), author_text.get(), year_text.get(),isbn_text.get()):
            list1.insert(END,row)

    def add_command(self):
        database.insert(title_text.get(), author_text.get(), year_text.get(),isbn_text.get())
        list1.delete(0,END)
        list1.insert(END, (title_text.get(), author_text.get(), year_text.get(),isbn_text.get()))

    def delete_command(self):
        database.delete(selected_tuple[0])

    def update_command(self):
        database.update(selected_tuple[0],title_text.get(), author_text.get(), year_text.get(),isbn_text.get())
