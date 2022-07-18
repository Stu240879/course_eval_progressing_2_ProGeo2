# this should be used to generate a report
# ToDo:
# figure out how FPDF works...
# make page with diagrams
# make page with tables
# make title page

# ### read this:
# # https://towardsdatascience.com/how-to-create-pdf-reports-with-python-the-essential-guide-c08dd3ebf2ee




# from fpdf import FPDF

# class PDF(FPDF):
#     def __init__(self):
#         super().__init__()
#         self.WIDTH = 210
#         self.HEIGHT = 297
        
#     def header(self):
#         # Custom logo and positioning
#         # Create an `assets` folder and put any wide and short image inside
#         # Name the image `logo.png`
#         # self.image('assets/logo.png', 10, 8, 33)
#         self.set_font('Arial', 'B', 11)
#         self.cell(self.WIDTH - 80)
#         self.cell(60, 1, 'Sales report', 0, 0, 'R')
#         self.ln(20)
        
#     def footer(self):
#         # Page numbers in the footer
#         self.set_y(-15)
#         self.set_font('Arial', 'I', 8)
#         self.set_text_color(128)
#         self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

#     def page_body(self, images):
#         # Determine how many plots there are per page and set positions
#         # and margins accordingly
#         if len(images) == 3:
#             self.image(images[0], 15, 25, self.WIDTH - 30)
#             self.image(images[1], 15, self.WIDTH / 2 + 5, self.WIDTH - 30)
#             self.image(images[2], 15, self.WIDTH / 2 + 90, self.WIDTH - 30)
#         elif len(images) == 2:
#             self.image(images[0], 15, 25, self.WIDTH - 30)
#             self.image(images[1], 15, self.WIDTH / 2 + 5, self.WIDTH - 30)
#         else:
#             self.image(images[0], 15, 25, self.WIDTH - 30)
            
#     def print_page(self, images):
#         # Generates the report
#         self.add_page()
#         self.page_body(images)


#     def pdfTable(self, data):
#         data = (
#             ("First name", "Last name", "Age", "City"),
#             ("Jules", "Smith", "34", "San Juan"),
#             ("Mary", "Ramos", "45", "Orlando"),
#             ("Carlson", "Banks", "19", "Los Angeles"),
#             ("Milano Roma Firenze Venezia Genova Napoli Livorno Bergamo Siracusa Rimini Pisa Bologna Brescia Torino"))
#         line_height = self.font_size * 2.5
#         col_width = self.epw / 4.5

#         lh_list = [] #list with proper line_height for each row
#         use_default_height = 0 #flag

#         #create lh_list of line_heights which size is equal to num rows of data
#         for row in data:
#             for datum in row:
#                 word_list = datum.split()
#                 number_of_words = len(word_list) #how many words
#                 if number_of_words>2: #names and cities formed by 2 words like Los Angeles are ok)
#                     use_default_height = 1
#                     new_line_height = self.font_size * (number_of_words/2) #new height change according to data 
#             if not use_default_height:
#                 lh_list.append(line_height)
#             else:
#                 lh_list.append(new_line_height)
#                 use_default_height = 0

#         #create your fpdf table ..passing also max_line_height!
#         for j,row in enumerate(data):
#             for datum in row:
#                 line_height = lh_list[j] #choose right height for current row
#                 self.multi_cell(col_width, line_height, datum, border=1,align='L',ln=3, 
#                 max_line_height=pdf.font_size)
#             self.ln(line_height)


from fpdf import FPDF

data = (
    ("First name", "Last name", "Age", "City"),
    ("Jules", "Smith", "34", "San Juan"),
    ("Mary", "Ramos", "45", "Orlando"),
    ("Carlson", "Banks", "19", "Los Angeles"),
    ("Milano Roma Firenze Venezia Genova Napoli Livorno Bergamo Siracusa Rimini Pisa Bologna Brescia Torino"),
    )
pdf = FPDF()
pdf.add_page()
pdf.set_font("Times", size=10)
line_height = pdf.font_size * 2.5
# col_width = pdf.epw / 4.5
col_width = pdf.fontsize / 4.5


lh_list = [] #list with proper line_height for each row
use_default_height = 0 #flag

#create lh_list of line_heights which size is equal to num rows of data
for row in data:
    for datum in row:
        word_list = datum.split()
        number_of_words = len(word_list) #how many words
        if number_of_words>2: #names and cities formed by 2 words like Los Angeles are ok)
            use_default_height = 1
            new_line_height = pdf.font_size * (number_of_words/2) #new height change according to data 
    if not use_default_height:
        lh_list.append(line_height)
    else:
        lh_list.append(new_line_height)
        use_default_height = 0

#create your fpdf table ..passing also max_line_height!
for j,row in enumerate(data):
    for datum in row:
        line_height = lh_list[j] #choose right height for current row
        pdf.multi_cell(col_width, line_height, datum, border=1,align='L',ln=3, 
        max_line_height=pdf.font_size)
    pdf.ln(line_height)

pdf.output('table_with_cells.pdf')