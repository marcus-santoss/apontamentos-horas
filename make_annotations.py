from core.imp_clockfy import ClockifyAnnotation

if __name__ == '__main__':
    # for provider in [JiraAnnotation, ClockifyAnnotation]:
    #     provider().fill_annotations(debug=True)̉

    j = ClockifyAnnotation()
    j.fill_annotations(debug=True)
