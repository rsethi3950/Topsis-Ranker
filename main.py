from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import FileField, FieldList, FloatField, SubmitField, RadioField, IntegerField
from flask_wtf.file import FileAllowed, FileRequired
app= Flask(__name__)
app.secret_key='my secret key'
class uploadForm(FlaskForm):
    File = FileField('Upload file', validators=[FileRequired(), FileAllowed(['csv'],'Only csv files allowed.')])
    cols = IntegerField('Number of columns in your file')
    select= RadioField("Do you wish to give weights to separate columns?",choices=[('Y',"Yes"),('N',"No")])
    submit = SubmitField()

class weightForm(FlaskForm):
    weights = FieldList(FloatField('weight'))
    send = SubmitField()
    def __init__(self, *args, **kwargs):
        cols = kwargs.pop('cols')
        super(weightForm, self).__init__(*args, **kwargs)
        self.weights.min_entries = cols

@app.route('/',methods=["GET","POST"])
def display():
    form=uploadForm()
    if request.method=="POST":
        
        if form.validate_on_submit():
            print('validated' , form.cols.data)
            return redirect(url_for('show_result', cols=form.cols.data))

        return render_template('base.html',form=form)
       
    return render_template('base.html',form=form)

@app.route('/result',methods=["GET","POST"])
def show_result():
    print(request.args.get('cols'))
    wform=weightForm(cols=request.args.get('cols'))
    # for x in range(request.args.get('cols')):
    #     wform.weights.append_entry()
    # for field in wform.weights:
    #     print (field())
    #     print
    if request.method=="GET":
        return render_template('result.html',form=wform, cols=request.args.get('cols'))
    return 'Done'

    


if __name__ == '__main__':
    app.run(debug=True)