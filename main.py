import cohere
from cohere.responses.classify import Example
#
# co = cohere.Client('1hBeXHXGg8WJ4HedMULMJxi0Br9opZ6tI3QeW76C')
examples=[
  Example("Where can I find a safe shelter for women in my area?", "Shelters"),
  Example("What kind of medical assistance is available for survivors of sexual assault?", "Medical assistance"),
  Example("Can you recommend a therapist who specializes in treating survivors of sexual assault?", "Therapy"),
  Example("What accommodations are available for survivors of sexual assault at universities?",
          "Academic accommodations"),
  Example("What can I do to improve my safety after a sexual assault?", "Safety concerns"),
  Example("How can I report a sexual assault to the police?", "Safety concerns"),
  Example("Are there any support groups for survivors of sexual assault in my area?", "Therapy"),
  Example("What kind of legal support is available for survivors of sexual assault?", "Safety concerns"),
  Example("How can I support a friend who has experienced sexual assault?", "Therapy"),
  Example("What should I do if I am experiencing flashbacks after a sexual assault?", "Therapy"),
  Example("How can I deal with anxiety after a sexual assault?", "Therapy"),
  Example("Can you recommend any books or resources for survivors of sexual assault?", "Therapy"),
  Example("What should I do if I am experiencing physical symptoms after a sexual assault?", "Medical assistance"),
  Example("How can I find a counselor who is experienced in working with LGBTQ+ survivors of sexual assault?",
          "Therapy"),
  Example("What should I do if I am experiencing depression after a sexual assault?", "Therapy"),
  Example("How can I find a support group for male survivors of sexual assault?", "Therapy"),
  Example("What kind of financial assistance is available for survivors of sexual assault?", "Safety concerns"),
  Example("What should I do if I am experiencing suicidal thoughts after a sexual assault?", "Therapy"),
  Example("How can I find a therapist who is experienced in working with survivors of childhood sexual abuse?",
          "Therapy"),
  Example("What should I do if I am experiencing PTSD after a sexual assault?", "Therapy"),
  Example("How can I find a counselor who is experienced in working with survivors of sex trafficking?", "Therapy"),
  Example("What kind of medical tests should I undergo after a sexual assault?", "Medical assistance"),
  Example("How can I protect myself from sexual assault in the future?", "Safety concerns"),
  Example("What kind of medical treatment is available for survivors of sexual assault?", "Medical assistance"),
  Example("What should I do if I am experiencing shame or guilt after a sexual assault?", "Therapy"),
  Example("How can I find a counselor who is experienced in working with survivors of military sexual trauma?",
          "Therapy"),
  Example("What should I do if I am experiencing nightmares after a sexual assault?", "Therapy"),
  Example("How can I find a therapist who is experienced in working with survivors of domestic violence?", "Therapy"),
  Example("What kind of legal rights do survivors of sexual assault have?", "Safety concerns"),
  Example("How can I find a counselor who is experienced in working with survivors of ritual abuse?", "Therapy"),
  Example("How can I request accommodations for exams or coursework after experiencing sexual assault?", "Academic accommodations"),
  Example("What kind of accommodations are typically available for survivors of sexual assault in college?", "Academic accommodations"),
  Example("How can I find out if my university has a Title IX office or program for survivors of sexual assault?", "Academic accommodations"),
  Example("Are there any resources for survivors of sexual assault who are struggling academically?", "Academic accommodations"),
  Example("How can I find a tutor or mentor who is experienced in working with survivors of sexual assault?", "Academic accommodations"),
  Example("How can I find a shelter that is specifically for LGBTQ+ survivors of sexual assault?", "Shelters"),
  Example("What kind of services are typically offered at a shelter for survivors of sexual assault?", "Shelters"),
  Example("Are there any shelters that allow pets for survivors of sexual assault?", "Shelters"),
  Example("How can I find a shelter that is wheelchair accessible for survivors of sexual assault with disabilities?", "Shelters"),
  Example("What should I do if all of the shelters in my area are full?", "Shelters"),

]
# inputs=["I am worried about my exam",]
#
# response = co.classify(
#   inputs=inputs,
#   examples=examples,
# )
# for classification in response:
#     labels = response.labels
#     probabilities = response.probabilities
# print(dir(response[0]))
# labels = []
# for classification in response:
#     labels.extend(classification.labels)

import flask
from flask import Flask,request,render_template
app = Flask(__name__,template_folder='templates')



question =''
inputs=''
@app.route('/', methods=["POST", "GET"])
def form():
     if request.method == "POST":
        global question
        question = request.form["question"]
        global inputs
        inputs=[question]
        print(question)
        return (get_response())

     return render_template('testtemplate.html')

print(inputs)
def get_model_response(inputs,examples):
  co = cohere.Client('hquGsqTx1Oyj8eThidC6bM3rzANHHnFZQNY92q2g')
  response = co.classify(inputs=inputs, examples=examples)
  return response
@app.route('/get_response')
def get_response():
    response = get_model_response(inputs,examples)
    labels = []
    for classification in response:
        labels.extend(classification.labels)

    prediction = []
    for classification in response:
        prediction.extend(classification.prediction)
    # probabilities = response.confidence
    if isinstance(classification.confidence, float):
        probabilities = [classification.confidence]
    # results = [{'prediction':prediction,  'probability': probabilities} for prediction, probability in zip(prediction, probabilities)]
    results = [{'label': c.prediction, 'probability': probabilities} for c in response.classifications]
    print(results)
    # print(type(results))
    # for result in results:
    #     if result['label'] == 'Shelters':
    #         suggestion = "Here are some <a href='https://github.com'>shelter resources</a>."
    #         return suggestion
    # return render_template('testresponse.html', results=results)
    suggestion = None

    for result in results:
        if result['label'] == 'Shelters':
            suggestion = "Seems that you are looking for shelters and maybe you want to check out <a href='https://sheltersafe.ca/'>the ShelterSafe website</a>. "
            # suggestion = "Here are some <a href='https://github.com'>shelter resources</a>."
            # suggestion = "<a class='suggestion-link' href='https://github.com'>Here are some shelter resources.</a>"
        elif result['label'] == "Medical assistance":
            suggestion = "Seems that you are looking for some medical assistance resources, here are some resources for you: <a href='https://endingviolencecanada.org/sexual-assault-centres-crisis-lines-and-support-services/'>Ending Violence Canada</a>; <a href='https://www.sadvtreatmentcentres.ca/find-a-centre/'>Find a treatment center near you</a>;  <a href='https://nbrhc.on.ca/programs-services/medical-services-2/sexual-assault-treatment-centre/'>What to expect from medical professionals (rape kit, follow up etc.)</a>. "
            # suggestion = "Here are some <a href='https://github.com'>medical resources</a>."
        elif result['label'] == "Therapy":
            suggestion = "Seems that you are looking for some therapy resources, here are some resources for you: <a href='https://www.psychologytoday.com/ca/therapists/ontario?category=sexual-abuse'>List of sexual abuse therapists in ontario</a>; <a href='https://www.betterhelp.com/advice/abuse/benefits-of-sexual-abuse-counseling/'>Better help councling</a>;  <a href='Charliehelp therapy targeted towards teens and young adults (11-30)'>Charliehelp therapy targeted towards teens and young adults (11-30)</a>. "
        elif result['label'] == "Academic accommodations":
            suggestion = "Seems that you are looking for information about academic accomodations, you might want to contact <a href='https://www.torontomu.ca/student-care/about/how-we-help/'>the TMU Student Care </a>. "
            # suggestion = "Here are some <a href='https://github.com'>academic accommodation resources</a>."
        elif result['label'] == "Safety concerns":
            suggestion = "If you want to build your own safety plan, consider contacting <a href='https://www.torontomu.ca/community-safety-security/personal-safety/'>TMU Community Safety and Security</a>. "
            # suggestion = "Here are some <a href='https://github.com'>safety resources</a>."

        print(suggestion)

    if suggestion:
        return render_template('testresponse.html', suggestion=suggestion)
    else:
        return ('no_suggestion')
    # for result in results:
    #     if result['label'] == 'Shelters':
    #         return ('Shelters Solution')
    #     elif result['label'] == "Medical assistance":
    #         return ("Medical assistance Solution")
    #     elif result['label'] == "Therapy":
    #         return ("Therapy Solution")
    #     elif result['label'] == "Academic accommodations":
    #         return ("Academic accommodations Solution")
    #     elif result['label'] == "Safety concerns":
    #         return ("Safety concerns Solution")

    # return render_template('testresponse.html', results=results)
if __name__ == '__main__':
    app.run(debug=True)