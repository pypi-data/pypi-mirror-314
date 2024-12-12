import tempfile

with tempfile.TemporaryDirectory() as temp_dir:
    print(f'Temporary directory created at: {temp_dir}')
    f = open(f"{temp_dir}/demofile2.txt", "w")
    f.write("Now the file has more content!")
    f.close()

    with open(f"{temp_dir}/demofile2.txt") as ff:
        print(ff.read()) 

print("- - - - - ")
with open(f"{temp_dir}/demofile2.txt") as ff:
    print(ff.read()) 