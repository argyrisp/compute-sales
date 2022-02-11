# -*- coding: utf-8 -*-
import os
def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

item_dict={}
afm_dict={}	
while(True):
	menu_input = input("Give your preference: (1: read new input file, 2: print statistics for a specific product, 3: print statistics for a specific AFM, 4: exit the program): ")
	if menu_input=="1":																                                                  #enter file
		file_name=input("Enter the input file name: ")
		file_path='./'+file_name
		if os.path.isfile(file_path):                                                                     #check if file exists
			f=open(file_name, "r", encoding='utf-8')
			empty_file_flag=False
			while(True):                                                                                    #loop that stops when dash is found
				fread_temp=f.read(1)
				if(fread_temp=="-"):
					break
				elif(fread_temp==""):
					empty_file_flag=True
					break
			if empty_file_flag:
				continue
			f.readline()
			
			while(True):                                                                                    #loop that reads through receipts
				receipt_list = []                                                                             #list of lines for specific receipt
				valid_flag=True
				sum=0
				current_line=f.readline()
				if(current_line is ""):
					break
				while(current_line[0]!="-"):                                                                  #store all lines that is supposed to be in the same receipt
					receipt_list.append(current_line.upper())
					current_line=f.readline()
					if(current_line is ""):
						break
				receipt_length=len(receipt_list)
				temp_dict={}
				
				if receipt_length==0:
					continue
				afm=receipt_list[0].split(":",1)
				if len(afm)!=2:
					continue
				afm[0]=afm[0].strip()
				afm[1]=afm[1].strip()
				
				total=receipt_list[receipt_length-1].split(":",1)
				if len(total)!=2:
					continue
				total[0]=total[0].strip()
				total[1]=total[1].strip()
				if(afm[0]!="ΑΦΜ" or not afm[1].isdigit() or len(afm[1])!=10):                                 #AFM check
					continue
				elif(total[0]!="ΣΥΝΟΛΟ" or not all([c.isdigit() or c == '.' for c in total[1]])): #total check
					continue
				for i in range(1,receipt_length-1):                                                           #after checking ΑΦΜ and ΣΥΝΟΛΟ lines, check the inbetween items
					item=receipt_list[i].split(":",1)
					if len(item)!=2:                                                                            #check if it only has 2 fields
						valid_flag=False
						break
					if item[0].strip()=="ΑΦΜ" or item[1].strip()=="ΣΥΝΟΛΟ":                                     #check if item name is AFM or SYNOLO
						valid_flag=False
						break
					item_numbers=item[1].split(None)
					if len(item_numbers) != 3 or not item_numbers[0].isdigit() :                                #check if it only has 3 fields 
						valid_flag=False
						break
					if not isfloat(item_numbers[1]) or not isfloat(item_numbers[2]):                            #check if first field is only digits, second and third only floats
						valid_flag=False
						break
					quantity=float(item_numbers[0])
					single_price=float(item_numbers[1])
					total_price=float(item_numbers[2])
					if abs(quantity*single_price-total_price)>0.000001:                                         #check if numbers of this line stand correct, with floating point error taken into consideration
						valid_flag=False
						break
					sum=sum+total_price
					if item[0] in temp_dict:
						temp_dict[item[0]] = round(temp_dict[item[0]] + total_price,2)
					else:
						temp_dict.update({item[0]: total_price})      		
				if not (valid_flag==True):
					continue
				if abs(sum - float(total[1])) > 0.000001:                                                     #check total price in comparison with the sum of each item's total price, with floating point error taken into consideration
					continue      
				key_list=list(temp_dict.keys())
				value_list=list(temp_dict.values())
				
						
				if(afm[1] in afm_dict):                                                                       #afm already in dictionary
					for temp in temp_dict.items():
						if temp[0] in afm_dict[afm[1]]:                                                           #fills the AFM key dictionary, menu option 3
							afm_dict[afm[1]][temp[0]]=round(afm_dict[afm[1]][temp[0]]+temp[1],2)
						else:
							afm_dict[afm[1]].update({temp[0]:temp[1]})
						if temp[0] in item_dict:                                                                  #fills the item key dictionary, menu option 2
							if(afm[1] in item_dict[temp[0]]):
								item_dict[temp[0]][afm[1]]=round(item_dict[temp[0]][afm[1]] + temp[1],2)
							else:
								item_dict[temp[0]].update({afm[1]:temp[1]})
						else:
							item_dict.update({temp[0]: {afm[1]: temp[1]}})
				else:
					afm_dict.update({afm[1]:temp_dict})                                                         #fills the AFM key dictionary, menu option 3
					for temp in temp_dict.items():                                                              #fills the item key dictionary, menu option 2
						if temp[0] in item_dict:
							if(afm[1] in item_dict[temp[0]]):
								item_dict[temp[0]][afm[1]]=round(item_dict[temp[0]][afm[1]] + temp[1],2)
							else:
								item_dict[temp[0]].update({afm[1]:temp[1]})
						else:
							item_dict.update({temp[0]: {afm[1]: temp[1]}})
	elif menu_input=="2":
		item_name_input=input("Enter item name: ").upper()
		if(item_name_input in item_dict):
			for temp in sorted(item_dict[item_name_input].items()):
				print(temp[0], " %0.2f" % float(temp[1]))
	elif menu_input=="3":
		afm_input=input("Enter afm: ").upper()
		if(afm_input in afm_dict):
			for temp in sorted(afm_dict[afm_input].items()):
				print(temp[0], " %0.2f" % float(temp[1]))
	elif menu_input=="4":
		break
