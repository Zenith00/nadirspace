import re

def parse(text):
    total = 0
    acq = 0
    for match in re.findall(r'<tr>.*?<\/tr>', text.replace("\n","")):
        # print(match)
        try:
            if "Adaptive" in match:
                for submatch in re.findall(r'(?<="col-points">).*(?= pts)', match):
                    acq += float(submatch.split(" / ")[0])
                pass

            else:
                for submatch in re.findall(r'(?<="col-points">).*(?= pts)', match):
                    acq += float(submatch.split(" / ")[0])
                    total += float(submatch.split(" / ")[1])
        except:
            pass
    return acq/total
