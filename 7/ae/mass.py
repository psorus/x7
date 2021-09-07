with open("main.py","r") as f:
    main=f.read()


def run(i):
    code=main
    code=code.replace("output",f"output{i}")
    code=code.replace("history",f"history{i}")
    exec(code)

if __name__=="__main__":
    for i in range(10):
        run(i)



