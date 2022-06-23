from flask import Flask, request, jsonify, render_template
from pytz import country_timezones,timezone
import pytz
from datetime import datetime
app = Flask(__name__)

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')



@app.route('/', methods = ['POST'])
def indexLogic():
    try:
        contents = request.get_json()

        # adminFromTime and adminToTime = the fromTime from input converted to hour + minutes (integer)
        xFrom = datetime.strptime(contents[0]['fromTime'], '%Y-%m-%dT%H:%M')
        adminFromTime = xFrom.hour + (xFrom.minute/60)

        xTo = datetime.strptime(contents[0]['toTime'], '%Y-%m-%dT%H:%M')
        adminToTime = xTo.hour + (xTo.minute/60)


        # fromTime and toTime will be the outputed times
        # Assumes the host will be availabe from 8am (UTC)
        # Assumes the host will be availabe till 6pm (UTC)
        fromTime = 8
        toTime = 18

        
        minTime = fromTime # the earliest time from all timezones 
        maxTime = toTime # the latest time from all timezones

        overlapedCCs = []
        weekendCCs = []

        for content in contents:
            # checks for weekends
            datetime_object = datetime.strptime(content['fromTime'], "%Y-%m-%dT%H:%M")
            if datetime_object.weekday() >= 5:
                weekendCCs.append(content['cc'])


            tzone = country_timezones[content['cc']]
            tzoneTime = datetime.now(pytz.timezone(((tzone[0])))).strftime("%z")


            sign = tzoneTime[0]
            hour = tzoneTime[1:3]
            minute = tzoneTime[3:]

            ttime = int(hour) + int(minute)/60 # elapsedTime from utc
            elapsedFromTime = 0
            elapsedToTime = 0
            if sign == '+':
                elapsedFromTime = adminFromTime + ttime
                elapsedToTime = adminToTime + ttime
            else:
                elapsedFromTime = adminFromTime - ttime
                elapsedToTime = adminToTime - ttime

            if elapsedFromTime < adminFromTime or elapsedToTime > adminToTime:
                overlapedCCs.append(content['cc']) # stores the overlapped country code

            if maxTime < elapsedToTime:
                maxTime = elapsedToTime
            
            if minTime > elapsedToTime:
                minTime = elapsedFromTime
        
        if(minTime < adminFromTime):
            fromTime += adminFromTime - minTime

        if(maxTime > adminToTime):
            toTime -=  maxTime - adminToTime


        if(fromTime < adminFromTime or toTime > adminToTime ):
            olap = ' '.join(map(str,overlapedCCs))
            return (jsonify({
                'success': 0,
                'message': 'There is an overlap of time in ' + olap,
                'status': 403
        }))

        elif(fromTime > adminToTime or toTime < adminFromTime ):
            
            return (jsonify({
                'success': 0,
                'message': 'There is an overlap of time in ' + olap,
                'status': 403
        }))

        elif(len(weekendCCs) > 0 ):
            weekendCC = ' '.join(map(str,weekendCCs))
            return (jsonify({
                'success': 0,
                'message': 'It is weekend in ' + weekendCC,
                'status': 403
        }))

        else:
            fromTime = int(fromTime)
            toTime = int(toTime)
            resp = {
                'fromTime' : f'{fromTime:02}00', 
                'toTime' : f'{toTime:02}00',
            }

            return (jsonify({
                'success': 1,
                'message': 'Available time fetched successfully',
                'data' : resp,
                'status': 200
            }))
    except Exception as e: 
        return (jsonify({
                'success': 0,
                'message': 'Invalid input! Please enter valid country code(s)',
                'status': 200
        }))


        
if __name__ == "__main__":
    app.run(debug=True)