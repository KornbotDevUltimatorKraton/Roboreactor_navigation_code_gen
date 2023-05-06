import os 
import json 
import requests 
import time 
from itertools import count

Account_data = "kornbot380@hotmail.com"
account_payload = {Account_data:"token_payload_input"} 
print(account_payload)
serial_nav_component = {} # Get the serial component port by the name of the part
cam_index_nav_component = {} #Get the camera index component by the name of the part  
server_url = "https://roboreactor.com/update_image"
for i in count(0):
            #try:
                  
                resq_dat = requests.post("https://roboreactor.com/gen_local_request",json=account_payload)
                print("Current_status json input ",resq_dat.json())  # Get the json input data from the json input 
                #Generat the  navigation type to send back the navigation component code into the system  
                nav_gen_code = resq_dat.json() # Get the json data of the api to get the code gen 
                status_nav = nav_gen_code.get('status') # Get the status navigation code data 
                if nav_gen_code != {}:  
                  if status_nav == "ON":
                               print("Activate the code generator features function ")
                               #First classify the hardware name on the system 
                               board_name_onboard = list(nav_gen_code.get("navigation_payload"))[0]   
                               #Get the project name here after updated server 
                               project_names = list(nav_gen_code.get("navigation_payload").get(board_name_onboard))[0] 

                               print(board_name_onboard,project_names) # Get the project name   
                               # Check if the computer onboard selected is on the selected function then begin function to generate the code
                               print("Total payload data ",nav_gen_code.get("navigation_payload").get(board_name_onboard))  
                               nav_options = nav_gen_code.get("navigation_payload").get(board_name_onboard).get(project_names) # Get the navigation list obtion 
                               device_name = nav_options.get("Navigation_wifi_name") # Get the wifi name from the list 
                               list_nav_compatible = {"Indoor_navigation":["Camera_navigation","Beacon_WiFi_navigation","Beacon_BLE_navigation"],"Outdoor_navigation":['point_cloud_3D','GPS','Lidar']}
                               list_data = os.listdir("/home/kornbotdev/Generate_navigation_code/")
                               if "navigation_function.py" in list_data:
                                            try:    
                                               os.remove("/home/kornbotdev/Generate_navigation_code/navigation_function.py")
                                            except:
                                                print("The file is already exist!")   
                               # Add the library           
                               code_nav_gen = open("navigation_function.py",'a')        
                               code_nav_gen.write("import os"+"\nimport cv2"+"\nimport serial"+"\nimport json"+"\nimport math"+"\nimport threading"+"\nimport subprocess"+"\nimport time"+"\nfrom itertools import count")
                               code_nav_gen.write("\nfrom navigation_lib import rssi_distance_report, Lidar_info_report,data_projection_post,Camera_image_sensor")
                               #Loop checking the serial device data to add the serial communication into the list data 
                                                              
                               #Generate the library of the components 
                               print("Check_name",list(nav_options))
                               code_nav_gen.write("\ndata_sensor = {}")
                               for nav_func in list(nav_options):
                                             print("Navigation option ",nav_func) 
                                             #Get the list data of the navigation component and generate the part first classify if there is the list of the serial component in the list navigation component or not 
                                             print("Get the instruction of nav components ",nav_func,nav_options[nav_func])

                                             #Get the serial generate from the list of instruction 
                                             #serial_nav_component         
                                             if "Select_usb_port" in list(nav_options[nav_func]):

                                                             print("Serial port _data",nav_func,nav_options[nav_func]['Select_usb_port'])
                                                             code_nav_gen.write("\ntry:"+"\n\tser_"+nav_func+" = serial.Serial('"+nav_options[nav_func]['Select_usb_port']+"',115200, timeout=1)"+"\nexcept:\n\tprint('Error serial connection please check your serial hardware connection')")
                                                             serial_nav_component[nav_func] = "ser_"+nav_func  
                                             #detecting the camera 
                                             if "camera_index" in list(nav_options[nav_func]):
                                                             print("Camera usb serial port selection port") 
                                                             camera_index_num = nav_options[nav_func]['camera_index']
                                                             code_nav_gen.write("\ncap_"+nav_func+" = cv2.VideoCapture("+str(camera_index_num)+")") # Get the index number input from the camera index to put into the camera input index generator 
                                                             #code_nav_gen.write("\nserver_url = 'https://roboreactor.com/update_image'")  # Image update url link to ativate from from the server 

                               for nav_func in list(nav_options):
                                              print("Generating the function of the navigation code ",nav_func) 
                                              # Add more navigation component both indoor and out door navigation system 
                                              #Indoor Navigation system 
                                              if nav_options[nav_func]['Navigation_component'] == 'Beacon_WiFi_navigation':
                                                             code_nav_gen.write("\ndef device_"+nav_func+"():"+"\n\twhile True:"+"\n\t\tdata_"+nav_func+" = rssi_distance_report('"+Account_data+"', '"+nav_func+"')")  
                                                             code_nav_gen.write("\n\t\tdata_sensor['"+nav_func+"'] = data_"+nav_func)
                                              if nav_options[nav_func]['Navigation_component'] == 'Beacon_BLE_navigation':
                                                             #Change this into the bluetooth version of the rssi code 
                                                             code_nav_gen.write("\ndef device_"+nav_func+"():"+"\n\twhile True:"+"\n\t\tdata_"+nav_func+" = rssi_distance_report('"+Account_data+"', '"+nav_func+"')")  
                                                             code_nav_gen.write("\n\t\tdata_sensor['"+nav_func+"'] = data_"+nav_func)
                                              if nav_options[nav_func]['Navigation_component'] == 'Camera_navigation':
                                                             code_nav_gen.write("\ndef device_"+nav_func+"():"+"\n\t\twhile True:")                              
                                                             code_nav_gen.write("\n\t\t\tCamera_image_sensor('"+Account_data+"','"+project_names+"',cap_"+nav_func+","+str(camera_index_num)+",'"+nav_func+"')")              
                                              #Out door navigation system
                                              if nav_options[nav_func]['Navigation_component'] == 'Lidar':                                                                      
                                                             code_nav_gen.write("\ndef device_"+nav_func+"():"+"\n\twhile True:"+"\n\t\tdata_"+nav_func+" = Lidar_info_report('"+Account_data+"', '"+nav_func+"',10000,ser_"+nav_func+")")
                                                             code_nav_gen.write("\n\t\tdata_sensor['"+nav_func+"'] = data_"+nav_func)
                                                
                               #Generate the data projection code to post data base into the system of the core communication system 
                               code_nav_gen.write("\ndef post_data_core():"+"\n\twhile True:"+"\n\t\tdata_projection = data_projection_post('"+Account_data+"',data_sensor)"+"\n\t\tprint(data_projection)")

                               for nav_func in list(nav_options):
                                              print("Generating the multithreading function for the multicore code generation ",nav_func) 
                                              code_nav_gen.write("\nt_"+nav_func+" = threading.Thread(target=device_"+nav_func+")"+"\nt_"+nav_func+".start()")
                                              
                               #Add the other thread for data projection 
                               code_nav_gen.write("\nt_post_projection = threading.Thread(target=post_data_core)"+"\nt_post_projection.start()")  
                               code_nav_gen.close()                     
                               resq_post = requests.post("https://roboreactor.com/gen_nav_change_status",json=account_payload)                 
                               print(resq_post.json())                
                               
                  if status_nav == "OFF":
                               print("Finish generating code of the navigation function algorithm") 
                               #resq_post = requests.post("https://roboreactor.com/gen_nav_change_status",json={account_payload})                 
                               #print(resq_post.json()) 
                  time.sleep(0.5)    
            #except:
            #     print("Error cannot connect to the server")
