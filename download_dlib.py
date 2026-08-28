import urllib.request
import bz2
import os

def download_file():
    url = "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"
    file_name = "shape_predictor_68_face_landmarks.dat.bz2"
    extracted_name = "shape_predictor_68_face_landmarks.dat"
    
    if os.path.exists(extracted_name):
        print("Already extracted.")
        return
        
    print("Downloading...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    count = 0
    with urllib.request.urlopen(req) as response, open(file_name, 'wb') as out_file:
        while True:
            chunk = response.read(8192 * 8)
            if not chunk: break
            out_file.write(chunk)
            count += len(chunk)
            if count % (1024 * 1024 * 10) == 0:
                print(f"Downloaded {count // (1024*1024)}MB...")
                
    print("Extracting...")
    with bz2.BZ2File(file_name, 'rb') as source, open(extracted_name, 'wb') as dest:
        dest.write(source.read())
    print("Done!")

if __name__ == "__main__":
    download_file()
