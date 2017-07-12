#################
# This file imports a list of adresses in csv format and produces another file
# that contains the address, the sq feet available for solar panels, and the 
# hours of usable sunlight per year using the Project Sunroof api 
#
# https://gist.github.com/shrav/7c7951ee7bd10b15f399
#################

import requests, csv

def generate_url(address):
    '''takes an address and generates its lat and lng to then 
    return the url of the sunroof api'''
    #find the lat and lng
    
    link = "http://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/find?text=" + str(address) +"&f=pjson"
    data = requests.get(link)
    datajson = data.json()

    
    if datajson['locations'] ==[]:
        return "lat,lng not found"
    else: 
        lng = datajson['locations'][0]['feature']['geometry']['x']
        lat = datajson['locations'][0]['feature']['geometry']['y']
        
        link = "https://www.google.com/async/sclp?async="
        url = link + "lat:" + str(lat) + ",lng:" + str(lng)    
        return url
    
def data(url):
    '''takes in the sunroof api url txt file and returns the ft and hrs '''
    
    #download and modify the data
    data = requests.get(url).content.decode("utf-8")
    data = data[4:-1]
    
    #extract the required info 
    ft = 'roof_good_solar_square_feet'
    hrs = 'yearly_hours_direct_sunlight'
    
    #slice to get only ft 
    ft_start = (data.find(ft)) + 29
    cut1 = (data[ft_start:])
    ft_end = cut1.find(",")
    ft_data = (cut1[:ft_end])
    
    #slice to get only hrs
    hrs_start = (data.find(hrs)) + 30
    cut2 = (data[hrs_start:])
    hrs_end = cut2.find(",")
    hrs_data = (cut2[:hrs_end])
    
    return (ft_data, hrs_data)
        
def main():
    '''opens a csv file of addresses and returns another csv with the address,
    the ft and hrs'''
    
    infile_name = input("Name of infile: ")
    outfile_name = input("Name of outfile: ")

    infile = open(infile_name, "r")
    csv_infile = csv.reader(infile)

     
    num_cols = len(next(csv_infile))
    infile.seek(0)
 
    if num_cols == 1:
        outfile = open(outfile_name, 'w', newline='')
        csv_outfile= csv.writer(outfile)
        header = ["Address", "sq ft available for solar panels", "hrs of usable sunlight per year"]
        csv_outfile.writerow(header)
        count = 0 

        for row in csv_infile:
            print (row)
            count += 1
            url = generate_url(row)
            if url == "lat,lng not found":
                row.append("lat,lng not found")
                row.append("lat,lng not found")
                csv_outfile.writerow(row)
    
            else:
                ft_data = data(url)[0]
                hrs_data = data(url)[1]
        
                row.append(ft_data)
                row.append(hrs_data)
        
                csv_outfile.writerow(row)
    
            print (count)
        print("yay, done!")
    else: 
        print ("oops, too many columns!")

    infile.close()
    outfile.close()
    
#main()

def main2():
    address = input("address: ")
    url = generate_url(address)
    print (data(url))

main2()    