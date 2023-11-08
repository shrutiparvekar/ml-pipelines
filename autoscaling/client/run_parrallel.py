import multiprocessing

def execute_python_script(script_name):
    try:
        exec(open(script_name).read())
    except Exception as e:
        print(f"Error executing {script_name}: {str(e)}")

if __name__ == "__main__":
    scripts = ["./client/test_classify.py", "./client/test_summarise.py", "./client/test_translate.py"]
    pool = multiprocessing.Pool(processes=len(scripts))
    pool.map(execute_python_script, scripts)
    pool.close()
    pool.join()
