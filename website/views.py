from flask import Blueprint, render_template

views = Blueprint("views", __name__)

@views.route('/')
@views.route('/home')
def aboutMe():
    return render_template('2_about_me.html')

@views.route('/resume')
def resume():
    return render_template('3_resume.html')

@views.route('/my_projects')
def myProjects():
    return render_template('4_my_projects.html')

@views.route('/contact_info')
def contactInfo():
    return render_template('5_contact_info.html')