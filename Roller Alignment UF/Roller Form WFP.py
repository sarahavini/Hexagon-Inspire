from System.IO  import *
import clr
import wpf
import imp
from numbers import Real
clr.AddReference("PresentationFramework")
clr.AddReference("PresentationCore")
clr.AddReference("windowsbase")
from System import Uri, UriKind
from System.Windows import (Application, Window, Thickness, HorizontalAlignment, VerticalAlignment, SizeToContent, Point, TextWrapping, TextAlignment, CornerRadius, HorizontalAlignment, VerticalAlignment, FontStyles)
from System.Windows.Documents import (Bold, Hyperlink, Italic, Run)
from System.IO import Path
from System.Windows.Controls import (Grid, ColumnDefinition, RowDefinition,CheckBox, ComboBox, ComboBoxItem, Label,Expander, TextBlock, TextBox, Button, StackPanel,InkCanvas, ScrollBarVisibility, ScrollViewer,Image, Border, ToolTip)
from System.Windows.Controls.Control import FontSize
from System.Windows.Media import (Brushes, SolidColorBrush, Colors, GradientStop, LinearGradientBrush, FontFamily, ImageSource)
from System.Windows.Shapes import Rectangle
from System.Windows.Media.Effects import DropShadowBitmapEffect, OuterGlowBitmapEffect
from System.Windows.Media.Imaging import BitmapImage

#******IMPORT EXTERNAL FUNCTIONS*********#
cmd = IN_GetScriptFullPath()
cmd.Run()
script_dir = os.path.dirname(cmd.ScriptPath)
imp.load_source("Roller_Alignment_V5", Path.Combine(script_dir, "Roller_Alignment_V5.py"))
import Roller_Alignment_V5

cmd = IN_GetScriptFullPath()
cmd.Run()
script_dir = os.path.dirname(cmd.ScriptPath)
imp.load_source("AdjustForm", Path.Combine(script_dir, "AdjustForm.py"))
import AdjustForm

#******CONFIGURE PAGE DISPLAY******#

#DEFINE A GRADIENT BACKGROUND FOR THE FORM
def GetLinearGradientBrush():
   brush = LinearGradientBrush()
   brush.StartPoint = Point(0,1)
   brush.EndPoint = Point(2,2)
   stops = [(Colors.DarkGray, 0.175),(Colors.DimGray, .1)]
   for color, stop in stops:
      brush.GradientStops.Add(GradientStop(color, stop))
   return brush
   
   
class ControlsExample(Window):
   def __init__(self):
      grid = self.getGrid(3,9)
      grid.Background = GetLinearGradientBrush()
      border = Border()
      border.BorderThickness = Thickness(1)
      border.Background = Brushes.White
      border.Padding = Thickness(.1)
      border.Child = grid
      self.Content = border
      self.addImage("C:\\Program Files\\Inspire\\VS CODE\\Roller Alignment UF\\picture1.png",1200,0,0,1)
      self.addValidationButton(6)
      self.addLabel("Choose Alignment Type",0,1,3)
      self.addAlignButton("All Rollers Square to Base Line",1,2,0)
      self.addAlignButton("All Rollers Parallel To Ref Roller, Ref Roller Floating",1,2,1)
      self.addAlignButton("All Rollers Parallel To Ref Roller, Ref Roller Square",1,2,2)
      self.addLabel("Choose Input Geometry Type",0,3,3)
      self.addGeomButton("Cylinders",1,4,0)
      #Circles
      #self.addGeomButton("Not Wired",1,4,1)
      #Axis Lines
      #self.addGeomButton("Not Wired",1,4,2)
      l=1

      self.addLabel("Enter Symetric Tolerance:",0,7,1)
      
      self.ProjNameBox = TextBox()
      self.ProjNameBox.Margin = Thickness(5)
      self.ProjNameBox.FontSize = 11
      self.ProjNameBox.Text = ''
      self.ProjNameBox.Width = 200 #75
      self.ProjNameBox.HorizontalAlignment = HorizontalAlignment.Center
      self.ProjNameBox.HorizontalContentAlignment = HorizontalAlignment.Center
      self.PositionOnGrid( self.ProjNameBox,0,2,7)

   #FUNCTION TO RETIREVE USER ENTRY FROM ENTRY BOX
   def SetProjName(self):
        global HightolPar
        global LowtolPar
        HightolPar = self.ProjNameBox.Text
        LowtolPar = float(HightolPar) * -1

   #FUNCTION TO ADD AN ENTRY BOX
   def addTxtBox(self, col, row):
      textBox = TextBox()
      textBox.Text = 'Symmetric Tolerance (inches)'
      textBox.FontSize = 11
      textBox.Width = 200 #75
      self.PositionOnGrid(textBox, 3, 1,0)

   #FUNCTION TO DEFINE GRID OF FORM
   def getGrid(self,Column,Row):
      grid = Grid()
      #grid.ShowGridLines = True
      for i in range(Column):
         grid.ColumnDefinitions.Add(ColumnDefinition())
      for i in range(Row):
         grid.RowDefinitions.Add(RowDefinition())
      return grid

   #FUNCTION TO ADD AN IMAGE TO THE FORM
   def addImage(self,image_path,width,col,row,nbcol):
      image = Image()
      image.MaxWidth = width
      image.Source = BitmapImage(Uri(image_path))
      image.HorizontalAlignment = HorizontalAlignment.Center
      image.VerticalAlignment = VerticalAlignment.Center
      self.PositionOnGrid(image,col,nbcol,row)
      
   #FUNCTION TO ADD A LABEL TO THE FORM
   def addLabel(self,text,col,row,nbcol):
      label = Label()
      label.Margin = Thickness(5)
      label.Content = text
      label.HorizontalAlignment = HorizontalAlignment.Center
      label.VerticalAlignment = VerticalAlignment.Center
      label.FontFamily = FontFamily(Uri(Path.GetFullPath(".\\Fonts\\")), "Arial Black")
      self.PositionOnGrid(label,col,nbcol,row)
    
   #FUNCTION TO ADD A SUBMIT BUTTON TO THE FORM
   def addValidationButton(self,ligne):
      button= Button()
      color = [0,0,0]
      button.Background = SolidColorBrush(Colors.Red)
      button.Content = "Submit"
      button.FontFamily = FontFamily(Uri(Path.GetFullPath(".\\Fonts\\")), "Calibri")
      button.FontSize = 36
      button.FontStyle = FontStyles.Italic
      button.Height = 25
      button.Width = 100
      button.BitmapEffect = OuterGlowBitmapEffect()
      button.Margin = Thickness(20)
      self.PositionOnGrid(button,5,7,8)
      def action(s, e):
         self.SetProjName()
         self.Close()
      button.Click += action

   #FUNCTION TO ADD BUTTON FOR ALIGNMENT TYPE OPTION
   def addAlignButton(self,content, col, row, horiz):
      button= Button()
      button.Background = Brushes.White
      button.Content = content
      button.FontFamily = FontFamily(Uri(Path.GetFullPath(".\\Fonts\\")), "Calibri")
      button.FontSize = 25
      button.Height = 25
      button.BitmapEffect = OuterGlowBitmapEffect()
      button.Margin = Thickness(20)
      self.PositionOnGrid(button,horiz,col,row)
      def action(s, e):
       global Alignment_Type
       Alignment_Type = str(content)

      button.Click += action
      
   #FUNCTION TO ADD BUTTON FOR GEOMETRY TYPE OPTION
   def addGeomButton(self,content, col, row, horiz):
      button= Button()
      button.Background = Brushes.White
      button.Content = content
      button.FontFamily = FontFamily(Uri(Path.GetFullPath(".\\Fonts\\")), "Calibri")
      button.FontSize = 25
      button.Height = 25
      button.BitmapEffect = OuterGlowBitmapEffect()
      button.Margin = Thickness(20)
      self.PositionOnGrid(button,horiz,col,row)
      def action(s, e):
       global Geom_Type
       Geom_Type = str(content)

      button.Click += action
      
   #FUNCTION TO PLACE AN ELEMENT ON FORM
   def PositionOnGrid(self, control, col, colnb,row):
      self.Content.Child.SetColumn(control,col)
      self.Content.Child.SetColumnSpan(control, colnb)
      self.Content.Child.SetRow(control, row)
      self.Content.Child.Children.Add(control)
            
#SHOW THE FORM           
window = ControlsExample()
window.ShowDialog()



#RETRIEVE USER INPUTS FROM FORM AFTER SUBMIT BUTTON IS CLICKED
if Alignment_Type == "All Rollers Square to Base Line":
   First_Roller_Alignment_Type = 0
if Alignment_Type == "All Rollers Parallel To Ref Roller, Ref Roller Square":
   First_Roller_Alignment_Type = 1
if Alignment_Type == "All Rollers Parallel To Ref Roller, Ref Roller Floating":
   First_Roller_Alignment_Type = 2
if Geom_Type == "Cylinders":
   Geom_Type_Calc = 0
if Geom_Type == "Circles":
   Geom_Type_Calc = 1
if Geom_Type == "Axis Lines":
   Geom_Type_Calc = 2

#Call the correct calculation script FOR THE ALIGNMENT TYPE PICKED
cmdF1 = IN_SetWorkingFrame("World")
cmdF1.Run()

global Flags
if First_Roller_Alignment_Type == 0 and Geom_Type_Calc == 0:
   Flags = Roller_Alignment_V5.AL0GEOM0(HightolPar, LowtolPar)
if First_Roller_Alignment_Type == 1 and Geom_Type_Calc == 0:
   Flags = Roller_Alignment_V5.AL1GEOM0(HightolPar, LowtolPar)
if First_Roller_Alignment_Type == 2 and Geom_Type_Calc == 0:
   Flags = Roller_Alignment_V5.AL2GEOM0(HightolPar, LowtolPar)
if First_Roller_Alignment_Type == 0 and Geom_Type_Calc == 1:
   Flags = Roller_Alignment_V5.AL0GEOM1(HightolPar, LowtolPar)

#AFTER FINISHING CALCULATIONS SHOW REPORT OUT PAGE

#FLAG SUM>0 MEANS AT LEAST ONE ROLLER WAS OUT OF TOLERANCE
global Flag_Sum
Flag_Sum = Flags[0] + Flags[1] + Flags[2]
#RETURN DICT CONTATINS ALL ROLLERS AND ADJUSTMENTS NEEDED
global return_dict 
return_dict = Flags[3]
#GENERAL VARIABLE TO HOLD THE NUMBER OF ROLLERS PRESENT IN JOB FILE
global NumRollers
NumRollers = Flags[4]

#IF A ROLLER HAS FAILED HAVE A RED BACKGROUND, IF ALL PASSED HAVE A GREEN BACKGROUND
def GetLinearGradientBrush():
   brush = LinearGradientBrush()
   brush.StartPoint = Point(0,1)
   brush.EndPoint = Point(2,2)
   if Flag_Sum > 0:
      stops = [(Colors.Red, 0.175),(Colors.DimGray, .1)]
   if Flag_Sum == 0: 
      stops = [(Colors.Green, 0.175),(Colors.DimGray, .1)]
   for color, stop in stops:
      brush.GradientStops.Add(GradientStop(color, stop))
   return brush

class ControlsExample(Window):
   def __init__(self):
      grid = self.getGrid(3,6)
      grid.Background = GetLinearGradientBrush()
      border = Border()
      border.BorderThickness = Thickness(1)
      border.Background = Brushes.White
      border.Padding = Thickness(.1)
      border.Child = grid
      self.Content = border
      self.addImage("C:\\Program Files\\Inspire\\VS CODE\\Roller Alignment UF\\picture1.png",500,0,0,1)
      self.addValidationButton(6)
      self.addExcelButton(5)
      print(Flag_Sum)
      if Flag_Sum<1:
         self.addLabel('Roller Alignment Within Specified Tolerance', 0,2,4)
      
      #FORMAT ROLLER FAIL PAGE
      if Flag_Sum > 0:
         global RollerNum
         RollerNum=1
         dictref=1
         row=0
         col=0
         #FOR EACH ROLLER ADD A BUTTON TO WINDOW WITH ITS NAME AS THE LABEL
         for entry in return_dict:
            st1 = return_dict[entry]
            if 'Ref' in st1 or "ref" in st1:
               Text = "Reference Roller 1"
               RollerNum=1
               row+=1
            else:
               Text = "Roller Number " + str(RollerNum) 
               row+=1
            if row>4:
               row=1
               col+=1
            dictref+=1
            self.addButton(Text, row,col)
            RollerNum+=1

   #FOR EACH ROLLERS BUTTON LINK A DETAILS FORM TO POP UP UPON CLICK
   def addButton(self,Text,ligne,col):
      global i
      i=0
      button= Button()
      color = [0,0,0]
      button.Background = SolidColorBrush(Colors.Red)
      button.Content = Text
      button.FontFamily = FontFamily(Uri(Path.GetFullPath(".\\Fonts\\")), "Calibri")
      button.FontSize = 36
      button.FontStyle = FontStyles.Italic
      button.Height = 25
      button.Width = 115
      button.BitmapEffect = OuterGlowBitmapEffect()
      button.Margin = Thickness(20)
      self.PositionOnGrid(button,col,1,ligne)
      def action(s, e):
         AdjustForm.test2(Text,return_dict)
      button.Click += action

   #FUNCTION TO SET GRID SIZE OF FORM
   def getGrid(self,Column,Row):
      grid = Grid()
      #grid.ShowGridLines = True
      # size of the grid
      for i in range(Column):
         grid.ColumnDefinitions.Add(ColumnDefinition())
      for i in range(Row):
         grid.RowDefinitions.Add(RowDefinition())
      return grid

   #FUNCITON TO ADD IMAGE TO FORM
   def addImage(self,image_path,width,col,row,nbcol):
      image = Image()
      #image.Margin = Thickness(25)
      image.MaxWidth = width
      #label.FontSize = 16
      image.Source = BitmapImage(Uri(image_path))
      #label.Foreground = Brushes.Cyan
      image.HorizontalAlignment = HorizontalAlignment.Center
      image.VerticalAlignment = VerticalAlignment.Center
      self.PositionOnGrid(image,col,nbcol,row)
      
   #FUNCITNO TO ADD LABEL TO FORM
   def addLabel(self,text,col,row,nbcol):
      label = Label()
      label.Margin = Thickness(5)
      #label.FontSize = 16
      label.Content = text
      #label.Foreground = Brushes.Cyan
      label.HorizontalAlignment = HorizontalAlignment.Center
      label.VerticalAlignment = VerticalAlignment.Center
      label.FontFamily = FontFamily(Uri(Path.GetFullPath(".\\Fonts\\")), "Arial Black")
      self.PositionOnGrid(label,col,nbcol,row)

   #FUNCITON TO ADD EXCEL BUTTON TO A FORM/OPENS EXCEL REPORT UPON CLICKING
   def addExcelButton(self,ligne):
      print(return_dict)
      button= Button()
      color = [0,0,0]
      button.Background = SolidColorBrush(Colors.Red)
      button.Content = "Report to Excel"
      button.FontFamily = FontFamily(Uri(Path.GetFullPath(".\\Fonts\\")), "Calibri")
      button.FontSize = 36
      button.FontStyle = FontStyles.Italic
      button.Height = 25
      button.Width = 100
      button.BitmapEffect = OuterGlowBitmapEffect()
      button.Margin = Thickness(20)
      self.PositionOnGrid(button,0,1,5)
      def action(s, e):
         #LAUNCH EXCEL
        clr.AddReference("Microsoft.Office.Interop.Excel")
        import Microsoft.Office.Interop.Excel as Excel
        excel = Excel.ApplicationClass()

        #WANT TO SEE EXCEL
        excel.Visible = True

        #ADD A NEW WORKBOOK
        wb = excel.Workbooks.Add()

        #ADD A NEW WORKSHEET
        ws = wb.Worksheets.Add()
        ws.Name = "RollerReport"

        #FORMAT EXCEL SHEET CHART HEADERS
        counter = 3
        i=0
        ws.Cells(1,1).Value="Cylinder Name"
        ws.Cells(1,2).Value="Needed Move X Direction"
        ws.Cells(1,3).Value="Needed Move Y Direction"
        ws.Cells(1,4).Value="Needed Move Z Direction"
        for entry in return_dict:
            dict_value = str(return_dict[i])
            dict_split = dict_value.split(',')
            name = dict_split[0]
            name = name[2:-1]
            x = dict_split[1]
            x = x[1:-1]
            y = dict_split[2]
            y = y[1:-1]
            z = dict_split[3]
            z = z[1:-2]
            ws.Cells(counter, 1).Value = name 
            ws.Cells(counter, 2).Value = (x)
            ws.Cells(counter, 3).Value = (y)
            ws.Cells(counter, 4).Value = (z)
            i+=1
            counter+=1
      button.Click += action

   #FUNCTION TO ADD SUBMIT BUTTON
   def addValidationButton(self,ligne):
      button= Button()
      color = [0,0,0]
      button.Background = SolidColorBrush(Colors.Red)
      button.Content = "Close"
      button.FontFamily = FontFamily(Uri(Path.GetFullPath(".\\Fonts\\")), "Calibri")
      button.FontSize = 36
      button.FontStyle = FontStyles.Italic
      button.Height = 25
      button.Width = 100
      button.BitmapEffect = OuterGlowBitmapEffect()
      button.Margin = Thickness(20)
      self.PositionOnGrid(button,4,3,ligne)
      def action(s, e):
       self.Close()
      button.Click += action
      
   #FUNCTION TO POSITION ELEMENT ON PAGE 
   def PositionOnGrid(self, control, col, colnb,row):
      self.Content.Child.SetColumn(control,col)
      self.Content.Child.SetColumnSpan(control, colnb)
      self.Content.Child.SetRow(control, row)
      self.Content.Child.Children.Add(control)
            
#SHOW THE FORM      
window = ControlsExample()
window.ShowDialog()