import clr
import wpf
import os
import sys
import imp
clr.AddReference("PresentationFramework")
clr.AddReference("PresentationCore")
clr.AddReference("windowsbase")
from numbers import Real
from re import X
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
from System.IO  import *

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
   def __init__(test):
      global i
      grid = test.getGrid(2,2)
      grid.Background = GetLinearGradientBrush()
      border = Border()
      border.BorderThickness = Thickness(1)
      border.Background = Brushes.White
      border.Padding = Thickness(.1)
      border.Child = grid
      test.Content = border
      test.addImage(imageloc, 600, 0,0,2)
      test.addValidationButton(6)
      test.addLabel(xtext,0,1,1)


   #FUNCTION TO ADD A LABEL TO PAGE
   def addLabel(self,text,col,row,nbcol):
      label = Label()
      label.Margin = Thickness(5)
      #label.FontSize = 16
      label.Content = text
      label.Foreground = Brushes.Cyan
      label.HorizontalAlignment = HorizontalAlignment.Center
      label.VerticalAlignment = VerticalAlignment.Center
      label.FontFamily = FontFamily(Uri(Path.GetFullPath(".\\Fonts\\")), "Arial Black")
      self.PositionOnGrid(label,col,nbcol,row)

   #FUNCTION TO SET GRID SIZE OF PAGE
   def getGrid(self,Column,Row):
      grid = Grid()
      #grid.ShowGridLines = True
      # size of the grid
      for i in range(Column):
         grid.ColumnDefinitions.Add(ColumnDefinition())
      for i in range(Row):
         grid.RowDefinitions.Add(RowDefinition())
      return grid

   #FUNCTION TO ADD IMAGE TO PAGE
   def addImage(self,image_path,width,col,row,nbcol):
      image = Image()
      image.MaxWidth = width
      image.Source = BitmapImage(Uri(Path.GetFullPath(image_path)))
      image.HorizontalAlignment = HorizontalAlignment.Center
      image.VerticalAlignment = VerticalAlignment.Center
      self.PositionOnGrid(image,col,nbcol,row)
   
   #CONTROL PLACEMENT OF ELEMENT ON PAGE
   def PositionOnGrid(self, control, col, colnb,row):
      self.Content.Child.SetColumn(control,col)
      self.Content.Child.SetColumnSpan(control, colnb)
      self.Content.Child.SetRowSpan(control, 2)
      self.Content.Child.SetRow(control, row)
      self.Content.Child.Children.Add(control)

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

def test2(Roller_Name,return_dict):
   #ORGANIZE RETURN_DICT
   numberspl = Roller_Name.split(' ')
   number = int(numberspl[2])
   number = number-1
   st1 = str(return_dict[number])
   st2 = st1.split(',')
   #SPLIT DICTIONARY ENTRIES INTO VARIABLES
   name = st2[0]
   x = st2[1]
   y = st2[2]
   z = st2[3]
   #TRIM RETURNS TO CONVERT TO FLOAT LATER
   x = x[2:10]
   y = y[2:10]
   z = z[2:10]
   #TEXT TO BE DISPLAYED ON WINDOW POP UP FOR ADJUSMENT NEEDED
   global xtext
   xtext = "Roller Number : " + str(number + 1) +", Adjustment: X " +str(x) + ", Z "+str(z)

   #DETERMINE WHICH PICTURE NEEDS TO BE ON POP UP WINDOW
   if float(x)<0:
      xstr = 'xneg'
   else:
      xstr = 'xpos'
   if float(z) <0:
      zstr = 'zneg'
   else:
      zstr = 'zpos'
   #GATHER IMAGE LOCATION
   global imageloc
   imageloc = "C:\\Program Files\\Inspire\\VS CODE\\Roller Alignment UF\\adjustment_" + xstr + zstr + '.png'

   #DISPLAY FORM
   window = ControlsExample()
   window.ShowDialog()