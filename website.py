from flask import Flask, render_template, request, send_file
from werkzeug import secure_filename
import requests, geocoder, csv

allowed_extensions = set(['csv'])
#upload_folder = 'C:\\Users\Recruiter-One\\Documents\\Diana\\Roof Website'

app = Flask(__name__)
app.config['DEBUG'] = True #auto-reflects changes in browser
#disable me in deployment

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/upload')
def upload():
    return render_template("upload.html")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in allowed_extensions

def generate_url(address):
    '''takes an address and generates its lat and lng to then 
    return the url of the sunroof api'''
    
    #find the lat and lng
    kwargs = {"key":"AIzaSyCagmGbhC3leQQjhjX_huZqLQIlkFLYMK0"}
    g = geocoder.google(str(address), **kwargs)
    
    if g.latlng == []:
        url = "lat,lng not found"
        
    else:
        lat = g.latlng[0]
        lng = g.latlng[1]
        
        #generate the link 
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
        
def run(infile_name, outfile_name):
    '''opens a csv file of addresses and returns another csv with the address,
    the ft and hrs'''

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
    
        return "worked"
    else: 
        return "did not work"

    infile.close()
    outfile.close()

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():    
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template("failed.html", reason = 'No file part')
        else:
            f = request.files['file']
            infile_name = f.filename
            if infile_name == "":
                return render_template("failed.html", reason ='No selected file')
            else:
                if f and allowed_file(f.filename):
                    f.save(secure_filename(f.filename))                    
                    #filename = secure_filename(f.filename)
                    #f.save(os.path.join(app.config['upload_folder'], filename))
                    outfile_name = "outfiletest1.csv"
                    
                    if run (infile_name, outfile_name) == "worked":
                        run(infile_name, outfile_name)
                        return render_template("success.html", infile_name = infile_name, outfile_name = outfile_name)
                    else: 
                        return render_template("failed.html", reason = 'Wrong file type, only .csv please')
                else: 
                    return render_template("failed.html", reason = 'Wrong file type, only .csv please')
    
@app.route('/uploader/<filename>')
def processed_file(filename):
    return send_file(filename)

#Error handling
@app.errorhandler(404) #error if no url is found
def not_found404(error):
    return "Sorry, I haven't coded that yet, I'll get back to you", 404
    #always add 404 at the end as convention 

@app.errorhandler(500)
def not_found500(error):
    return "My code broke, my bad", 500
    #always add 404 at the end as convention     
#if __name__ == '__main__':
    #app.run(host='0.0.0.0')
