round_ = (value, places=2) ->
    multi = Math.pow(10, places)
    return Math.round(value * multi) / multi


updateTooltip = (x) ->
    for chart in Highcharts.charts
        chart.tooltip.refresh([chart.series[0].points[x]])
        chart.series[0].data[x].setState('hover')


getActivityId = () ->
    url = document.location.pathname.split '/'
    return url[url.length - 1]


groupData = (data) ->
    min = data[0][0]  # valid because data is sorted
    max = data[data.length - 1][0]
    increment = Math.ceil((max - min) / 25)

    local_max = min + increment
    new_data = []
    i = 0
    count = 0
    for point in data
        if local_max < point[0]
            i += 1
            local_max += increment

        count += point[1]
        if new_data[i]?
            new_data[i][1] += point[1]
        else
            new_data[i] = []
            new_data[i][0] = local_max - increment
            new_data[i][1] = point[1]

    return [
        new_data
        count
    ]


toSIBase = (value, units) ->
    multi = 1

    if units.charAt(0) == 'k'
        multi *= 1000

    if units == 'mile'
        multi *= 1609

    if units == 'ft'
        multi *= 0.3048

    if units == 'min'
        multi *= 60

    if units == 'h'
        multi *= 3600

    return value * multi


formatTime = (value, has_seconds=false) ->
    seconds = value % 60
    minutes = value // 60 % 60
    hours = value // 3600

    str_min = if minutes < 10 then "0#{minutes}" else "#{minutes}"
    if not has_seconds
        return "#{hours}:#{str_min}"
    else
        str_sec = if seconds < 10 then "0#{seconds}" else "#{seconds}"
        return "#{hours}:#{str_min}:#{str_sec}"


formatDistance = (value) ->
    if SI_UNITS
        multi = 1 / 1000
    else
        multi = 1 / 1609

    val = value * multi
    round_precision = if val < 1 then 2 else 1

    d_str = round_(value * multi, round_precision)
    return "#{d_str} #{UNITS.distance}"

formatShortDistance = (value) ->
    if SI_UNITS
        multi = 1
    else
        multi = 3.281

    d_str = round_(value * multi, 0)
    return "#{d_str} #{UNITS.height}"

formatSpeed = (value) ->
    if SI_UNITS
        multi = 3.6
    else
        multi = 2.237

    s_str = round_(value * multi, 1)
    return "#{s_str} #{UNITS.speed}"


#############
# Ochart
#############

createOchart = (data, height=200) ->
    multi_speed = if SI_UNITS then 3.6 else 2.237
    data[1] = ([e[0], round_(e[1] * multi_speed, 2)] for e in data[1])

    if not SI_UNITS
        data[0] = ([e[0], round_(e[1] * 3.281, 0)] for e in data[0])

    $('#ochart').highcharts
        chart:
            height: height
        credits:
            enabled: false
        legend:
            enabled: false
        title:
            text: null
        plotOptions:
            series:
                point:
                    events:
                        mouseOver: (event) ->
                            movePointerEvent this.index
        tooltip:
            shared: true
            crosshairs: true
            formatter: ->
                distance = this.x / 1000 + " #{UNITS.distance}"
                elevation = this.points[0].y + " #{UNITS.height}"
                speed = this.points[1].y + " #{UNITS.speed}"

                return "<b>#{distance}</b><br>Elevation: #{elevation}<br>Speed: #{speed}"
        series: [
            name: 'Elevation'
            data: data[0]
            yAxis: 0
        ,
            name: 'Speed'
            data: data[1]
            yAxis: 1
        ]
        xAxis:
            labels:
                formatter: ->
                    return this.value / 1000 + " #{UNITS.distance}"
        yAxis: [
            id: 0
            title:
              enabled: false
            labels:
              formatter: ->
                return this.value + " #{UNITS.height}"
        ,
            id: 1
            min: 0
            labels:
                align: 'left'
                formatter: ->
                    return this.value + " #{UNITS.speed}"
            opposite: true
            title:
                enabled: false
        ]


#############
# Charts
#############

createChart = (target, name, color, data, units) ->
    $(target).highcharts
        chart:
            height: 150
        colors: [color]
        credits:
            enabled: false
        legend:
            enabled: false
        plotOptions:
            series:
                point:
                    events:
                        mouseOver: (event) ->
                            updateTooltip this.index
        title:
            text: name
            floating: true
        tooltip:
            shared: true
            crosshairs: true
            formatter: ->
                distance = round_(this.x / 1000, 2) + " #{UNITS.distance}"
                val = this.points[0].y + " #{units}"

                return "<b>#{distance}</b><br>#{name}: #{val}"
        series: [
            name: name
            data: data
        ]
        xAxis:
            labels:
                formatter: ->
                    return this.value / 1000 + " #{UNITS.distance}"
        yAxis: [
            id: 0
            min: Math.min.apply null, (v[1] for v in data)
            title:
              enabled: false
            labels:
              formatter: ->
                return this.value + " #{units}"
        ]

createElevationChart = (data) ->
    if not SI_UNITS
        data = ([e[0], round_(e[1] * 3.281, 0)] for e in data)

    createChart '#elevation_chart', 'Elevation', 'red', data, UNITS.height

createSpeedChart = (data) ->
    multi_speed = if SI_UNITS then 3.6 else 2.237
    data = ([e[0], round_(e[1] * multi_speed, 2)] for e in data)

    createChart '#speed_chart', 'Speed', 'green', data, UNITS.speed

createGradeChart = (data) ->
    createChart '#grade_chart', 'Grade', 'blue', data, UNITS.percent

createHrChart = (data) ->
    createChart '#hr_chart', 'Heart rate', 'orange', data, UNITS.per_min

createCadChart = (data) ->
    createChart '#cad_chart', 'Cadence', 'pink', data, UNITS.per_min

createTempChart = (data) ->
    if not SI_UNITS
        data = ([e[0], round_(e[1] * 1.8 + 32, 0)] for e in data)

    createChart '#temp_chart', 'Temperature', 'purple', data, UNITS.temperature


#############
# Zones
#############

createZones = (target, name, color, data, units) ->
    [data, count] = groupData(data)

    for val, i in data
        data[i][1] = val[1] / count * 100

    $(target).highcharts
        chart:
            type: 'column'
            height: 200
        colors: [color]
        credits:
            enabled: false
        legend:
            enabled: false
        title:
            text: name
            floating: true
        tooltip:
            shared: true
            crosshairs: true
            formatter: ->
                val = this.x + " #{units}"
                percent = round_(this.points[0].y, 2) + " %"

                return "<b>#{val}</b><br>#{percent}"
        series: [
            name: name
            data: data
        ]
        xAxis:
            labels:
                formatter: ->
                    return this.value + " #{units}"
        yAxis: [
            id: 0
            title:
              enabled: false
            labels:
              formatter: ->
                return this.value + " %"
        ]


createElevationZones = (data) ->
    if not SI_UNITS
        data = ([e[0], round_(e[1] * 3.281, 0)] for e in data)

    createZones '#elevation_zones', 'Elevation', 'red', data, UNITS.height

createSpeedZones = (data) ->
    multi_speed = if SI_UNITS then 3.6 else 2.237
    data = ([e[0], round_(e[1] * multi_speed, 2)] for e in data)

    createZones '#speed_zones', 'Speed', 'green', data, UNITS.speed

createGradeZones = (data) ->
    createZones '#grade_zones', 'Grade', 'blue', data, UNITS.percent

createHrZones = (data) ->
    createZones '#hr_zones', 'Heart rate', 'orange', data, UNITS.per_min

createCadZones = (data) ->
    createZones '#cad_zones', 'Cadence', 'pink', data, UNITS.per_min

createTempZones = (data) ->
    if not SI_UNITS
        data = ([e[0], round_(e[1] * 1.8 + 32, 0)] for e in data)

    createZones '#temp_zones', 'Temperature', 'purple', data, UNITS.temperature


#############
# Map
#############

convertTrack = (points) ->
    latLng = []
    extremes =
        x:
            min: 180
            max: -180
        y:
            min: 90
            max: -90

    for point in points
        x = point[0]
        y = point[1]

        latLng.push new google.maps.LatLng x, y

        if x < extremes.x.min
            extremes.x.min = x
        else if x > extremes.x.max
            extremes.x.max = x

        if y < extremes.y.min
            extremes.y.min = y
        else if y > extremes.y.max
            extremes.y.max = y

    return {
        extremes: extremes
        points: latLng
    }

getBounds = (extremes) ->
    bounds = new google.maps.LatLngBounds

    min = new google.maps.LatLng extremes.x.min, extremes.y.min
    max = new google.maps.LatLng extremes.x.max, extremes.y.max
    bounds.extend min
    bounds.extend max

    return bounds


points = null
pointer = null
setMovePointerEvent = (ptr, pts) ->
    pointer = ptr
    points = pts


movePointerEvent = (index) ->
    if not pointer or not points
        return

    pointer.setPosition points[index]


createMap = (data) ->
    track = convertTrack data
    center = new google.maps.LatLng (track.extremes.x.max + track.extremes.x.min) / 2, (track.extremes.y.max + track.extremes.y.min) / 2
    bounds = getBounds track.extremes

    map = new google.maps.Map document.getElementById('map'), {
            zoom: 10,
            center: center,
            mapTypeId: google.maps.MapTypeId.TERRAIN
        }
    map.fitBounds bounds

    polyline = new google.maps.Polyline
      path: track.points
      strokeColor: '#FF0000'
      strokeOpacity: 1.0
      strokeWeight: 4
      editable: false

    polyline.setMap map

    marker = new google.maps.Marker
        icon:
            path: google.maps.SymbolPath.CIRCLE
            scale: 7
            fillColor: '#6CC9EB'
            fillOpacity: 1.0
            strokeColor: '#FFFFFF'
            strokeOpacity: 1.0
            strokeWeight: 2

    setMovePointerEvent marker, track.points
    marker.setMap map

#############
# Best splits
#############

findBestSplits = (data) ->
    $('td[data-best-split]').each ->
        args = parseSplitArgs $(this).attr('data-best-split')

        if args.what in ['cad', 'hr', 'elevation']
            interval = if args.type == 'distance' then args.interval * 100 else args.interval
            si_val = bestSplitGeneric data[args.type], data[args.what], interval, false
            $(this).text if args.what == 'elevation' then formatShortDistance si_val else si_val
        else if args.what == 'speed'
            interval = if args.type == 'distance' then args.interval * 100 else args.interval
            si_val = bestSplitSpeed data.time, data.distance, interval, args.type == 'time'
            $(this).text formatSpeed si_val
        else
            interval = if args.type == 'distance' then args.interval * 100 else args.interval
            si_val = bestSplitGeneric data[args.type], data[args.what], interval, true, args.type == 'distance'
            $(this).text if args.type == 'time' then formatDistance si_val / 100 else formatTime si_val, true

parseSplitArgs = (str) ->
    attrs = str.split('-')

    interval = toSIBase(parseFloat(attrs[1]), attrs[2])

    return {
        what: attrs[0]
        type: if attrs[2] in ['s', 'min', 'h'] then 'time' else 'distance'
        interval: interval
    }


bestSplitGeneric = (control, data, interval, as_delta=true, prefer_min=false) ->
    choose_best = if prefer_min then Math.min else Math.max
    best = if prefer_min then Number.MAX_VALUE else 0
    [start, delta, current] = initialSum control, data, interval, as_delta

    prev = data[start - 1]
    j = 0  # pointer to last element in subarray
    for d, i in data[start..]
        if as_delta
            current += d
        else
            current += d - prev
            prev = d

        delta += control[i + start]

        if delta > interval
            best = choose_best(current, best)

            while delta > interval
                if as_delta
                    current -= data[j]
                else
                    current -= if data[j - 1] then data[j] - data[j - 1] else 0

                delta -= control[j]
                j += 1

    return best


bestSplitSpeed = (time, distance, interval, interval_time=true) ->
    best = 0
    control = if interval_time then time else distance

    [start, delta, c_dist] = initialSum control, distance, interval, true
    c_time = (initialSum control, time, interval, true)[2]

    j = 0  # pointer to last element in subarray
    for c, i in control[start..]
        c_time += time[i + start]
        c_dist += distance[i + start]
        delta += c

        if delta > interval
            best = Math.max(round_(c_dist / c_time / 100, 1), best)

            while delta > interval
                c_time -= time[j]
                c_dist -= distance[j]
                delta -= control[j]
                j += 1

    return best


initialSum = (control, data, interval, as_delta=true) ->
    sum = 0
    delta = 0
    i = 0
    prev = data[0]

    while delta < interval and i < data.length
        i += 1
        if as_delta
            sum += data[i]
        else
            sum += data[i] - prev
            prev = data[i]

        delta += control[i]

    return [i, delta, sum]


changeSummary = () ->
    period = do $('#summary_for').val
    $.getJSON "/activities/api/summary/#{period}", (json) ->
        for target, value of json
            switch target
                when 'total_time' then $("##{target}").text formatTime value
                when 'longest' then $("##{target}").text formatTime value
                when 'avg_duration' then $("##{target}").text formatTime value
                when 'farthest' then $("##{target}").text formatDistance value
                when 'total_distance' then $("##{target}").text formatDistance value
                when 'avg_distance' then $("##{target}").text formatDistance value
                when 'max_speed' then $("##{target}").text formatSpeed value / 360
                when 'avg_speed' then $("##{target}").text formatSpeed value
                when 'elev_gain' then $("##{target}").text formatShortDistance value
                else $("##{target}").text if value != null then value else 0


createWchart = (data) ->
    $('#wchart').highcharts
        chart:
            type: 'column'
            height: 300
        credits:
            enabled: false
        legend:
            enabled: false
        title:
            text: name
            floating: true
        tooltip:
            shared: true
            crosshairs: true
            formatter: ->
                return "<b>Dist</b>: #{this.points[0].y / 1000} #{UNITS.distance}<br><b>Time</b>: #{formatTime(this.points[1].y)}<br><b>Rating</b>: #{this.points[2].y}<br><b>#</b>: #{this.points[3].y}"
        series: [
            name: 'Distance'
            data: data.distance
            yAxis: 0
        ,
            name: 'Time'
            data: data.time
            yAxis: 1
        ,
            name: 'Rating'
            data: data.rating
            yAxis: 2
        ,
            name: 'N'
            data: data.n
            yAxis: 3
        ]
        xAxis:
            labels:
                formatter: ->
                    return this.value
        yAxis: [
            id: 0
            title:
                text: 'Distance'
                enabled: false
            labels:
                enabled: false
                formatter: ->
                    return this.value / 1000 + " #{UNITS.distance}"
        ,
            id: 1
            title:
                text: 'Time'
                enabled: false
            labels:
                enabled: false
                formatter: ->
                    return formatTime this.value
        ,
            id: 2
            opposite: true
            title:
                text: 'Rating'
                enabled: false
            labels:
                enabled: false
                formatter: ->
                    return this.value
        ,
            id: 3
            opposite: true
            title:
                text: '#'
                enabled: false
            labels:
                enabled: false
                forrmatter: ->
                    return this.value
        ]


$ ->
    do $('select').selecter
    do $('[data-toggle="tooltip"]').tooltip

    id = do getActivityId

    $('[data-action="delete-activity"]').click (e) ->
        if not confirm 'Are you sure you want to delete this activity?'
            do e.preventDefault

    if $('#id_date').length
        new Pikaday
            field: $('#id_date')[0]
            format: 'YYYY-MM-DD'

    if $('#map').length
        $.getJSON "/activities/api/map/#{id}", (json) ->
            createMap json

    if $('.bm-nav').length
        $.getJSON "/activities/api/ochart/#{id}", (json) ->
            createOchart json, 150
    else if $('#ochart').length
        $.getJSON "/activities/api/ochart/#{id}", (json) ->
            createOchart json

    if $('#elevation_chart').length
        $.getJSON "/activities/api/chart/#{id}/elevation", (json) ->
            createElevationChart json

    if $('#speed_chart').length
        $.getJSON "/activities/api/chart/#{id}/speed", (json) ->
            createSpeedChart json

    if $('#grade_chart').length
        $.getJSON "/activities/api/chart/#{id}/grade", (json) ->
            createGradeChart json

    if $('#hr_chart').length
        $.getJSON "/activities/api/chart/#{id}/hr", (json) ->
            createHrChart json

    if $('#cad_chart').length
        $.getJSON "/activities/api/chart/#{id}/cadence", (json) ->
            createCadChart json

    if $('#temp_chart').length
        $.getJSON "/activities/api/chart/#{id}/temperature", (json) ->
            createTempChart json

    if $('#elevation_zones').length
        $.getJSON "/activities/api/zones/#{id}/elevation", (json) ->
            createElevationZones json

    if $('#speed_zones').length
        $.getJSON "/activities/api/zones/#{id}/speed", (json) ->
            createSpeedZones json

    if $('#grade_zones').length
        $.getJSON "/activities/api/zones/#{id}/grade", (json) ->
            createGradeZones json

    if $('#hr_zones').length
        $.getJSON "/activities/api/zones/#{id}/hr", (json) ->
            createHrZones json

    if $('#cad_zones').length
        $.getJSON "/activities/api/zones/#{id}/cadence", (json) ->
            createCadZones json

    if $('#temp_zones').length
        $.getJSON "/activities/api/zones/#{id}/temperature", (json) ->
            createTempZones json

    if $('td[data-best-split]').length
        $.getJSON "/activities/api/track/#{id}", (json) ->
            findBestSplits json

    if $('#summary_for').length
        do changeSummary
        $('#summary_for').change changeSummary

    if $('#wchart').length
        $.getJSON "/activities/api/wchart", (json) ->
            createWchart json
