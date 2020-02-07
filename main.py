from flask import Flask, render_template, request, session
import conn
import json
app=Flask(__name__)

@app.route('/login')
def user_login():
	return render_template('login.html')

@app.route('/log_ver', methods=['GET', 'POST'])
def log_ver():
	res = conn.login(request.form['uname'], request.form['pwd'])
	if res:
		session['uname'] = request.form['uname']
		if res[0][2] == 'admin':
			return render_template('admindash.html')
		elif res[0][2] == 'college':
			return render_template('clgdash.html')
		elif res[0][2] == 'teacher':
			return render_template('tchdash.html')
		elif res[0][2] == 'student':
			return render_template('studash.html')
	else:
		print('no')
		return render_template('login.html')

@app.route('/comanage')
def course_manage():
	res = conn.getcourse()
	print(res)
	return render_template('adcomanage.html', a = res)

@app.route('/create_course', methods=['GET', 'POST'])
def create_course():
	print('hello')
	conn.createcourse(request.form['cname'], request.form['categ'], request.form['stream'], request.form['type'], request.form['durtn'], request.form['mod'])
	return "Course has been Created Successfully"

@app.route('/update_course', methods=['GET', 'POST'])
def update_course():
	conn.updatecourse(request.form['cid'], request.form['cname'], request.form['categ'], request.form['stream'], request.form['type'], request.form['durtn'], request.form['mod'])
	return "Course has been Updated Successfully"

@app.route('/delete_course', methods=['GET', 'POST'])
def delete_course():
	conn.deletecourse(request.form['cid'])
	return "Course has been Deleted Successfully"

@app.route('/logout')
def logout():
	session.clear()
	return render_template('login.html')

@app.route('/cregister')
def colg_register():
	return render_template('clregister.html')

@app.route('/create_college', methods=['GET', 'POST'])
def create_college():
	conn.createcollege(request.form['clname'], request.form['clstate'], request.form['cldist'], request.form['clcity'],request.form['clpin'], request.form['clph'], request.form['clemail'], request.form['uname'])
	conn.getlgdata(request.form['uname'], request.form['pwd'], 'college')
	return "College has been Registered Successfully"

@app.route('/clmanage')
def college_manage():
	res = conn.getcollege()
	print(res)
	return render_template('adclmanage.html', a = res)

@app.route('/aprv_usr', methods=['GET', 'POST'])
def aprv_colg():
	print(request.form['uname'])
	conn.aprvcolg(request.form['uname'])
	return "User has been Approved Successfully"

@app.route('/daprv_usr', methods=['GET', 'POST'])
def daprv_colg():
	print(request.form['uname'])
	conn.daprvcolg(request.form['uname'])
	return "User has been Disapproved Successfully"

@app.route('/clcourse')
def colcourse():
	res1 = conn.getdcourse(session['uname'])
	res2 = conn.getucourse(session['uname'])
	print(res2)
	return render_template("clcourse.html", a = res1, b = res2)

@app.route('/dclr_course', methods=['GET', 'POST'])
def dclr_course():
	conn.dclrcourse(request.form['cid'], session['uname'])
	return "Course has been Declared Successfully"

@app.route('/clg_course', methods=['GET', 'POST'])
def clg_course():
	res = conn.getclgcourse(request.form['cid'])
	r = ""
	for i in res:
		r = r + """<option value="""+str(i[0])+""">"""+str(i[1])+"""</option>"""
	return r

@app.route('/sumanage')
def subject_manage():
	r = conn.getcourse()
	res = []
	for i in r:
		res.append((i[0], i[1]))
	return render_template('adsumanage.html', a = res)
	
@app.route('/get_sub', methods=['GET', 'POST'])
def get_sub():
	res = conn.getsub(request.form['cid'])
	print('gggg', res)
	if res:
		r = """<div class="card shadow mb-4">
				<div class="card-header py-3">
				<h6 class="m-0 font-weight-bold text-primary">Subjects List</h6>
				</div>
				<div class="card-body">
				<div class="table-responsive">
					<table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
					<thead>
						<tr>
						<th>ID</th>
						<th>Name</th>
						<th>Type</th>
						<th>Semester</th>
						<th>No of Modules</th>
						</tr>
					</thead>
					<tbody>"""
		for i in res:
			r = r + """<tr>
						<td style="cursor: pointer;" data-toggle="modal" data-target="#sub_updt_modal"
                        onclick="updt('"""+ str(i[0]) +"""', '"""+ str(i[1]) +"""', '"""+ str(i[2]) +"""', '"""+ str(i[3]) +"""', '"""+ str(i[4]) +"""', '"""+ str(i[5]) +"""')">"""+ str(i[0]) +"""</td>
						<td>"""+ str(i[1]) +"""</td>
						<td>"""+ str(i[2]) +"""</td>
						<td>"""+ str(i[3]) +"""</td>
						<td>"""+ str(i[4]) +"""</td>
						</tr>"""
		r = r + """ </tbody>
					</table>
				</div>
				</div>
			</div>"""
		return r

@app.route('/cre_sub', methods=['GET', 'POST'])
def cre_sub():
	conn.cresub(request.form['cid'], request.form['sbname'], request.form['sbtype'],request.form['sbsem'], request.form['sbmod'])
	return "Subject created successfully"

@app.route('/tregister')
def tchr_register():
	r = conn.getcollege()
	print(r)
	res = []
	for i in r:
		if i[9] == 1:
			res.append((i[0], i[1]))
	return render_template('thregister.html', a = res)

@app.route('/crs_subject', methods=['GET', 'POST'])
def crs_subject():
	res = conn.crssubject(request.form['cid'])
	r = ""
	for i in res:
		r = r + """<option value="""+str(i[0])+""">"""+str(i[1])+"""</option>"""
	return r

@app.route('/create_teacher', methods=['GET', 'POST'])
def create_teacher():
	conn.createteacher(request.form['trname'], request.form['trgendr'], request.form['trstate'], request.form['trdist'], request.form['trcity'], request.form['trpin'], request.form['trph'], request.form['tremail'], request.form['trcrs'], request.form['clid'], request.form['uname'])
	conn.getlgdata(request.form['uname'], request.form['pwd'], 'teacher')
	return "Teacher has been Registered Successfully"

@app.route('/sregister')
def std_register():
	r = conn.getcollege()
	print(r)
	res = []
	for i in r:
		if i[9] == 1:
			res.append((i[0], i[1]))
	return render_template('stregister.html', a = res)

@app.route('/create_student', methods=['GET', 'POST'])
def create_student():
	conn.createstudent(request.form['stname'], request.form['stgendr'], request.form['stage'], request.form['ststate'], request.form['stdist'], request.form['stcity'], request.form['stpin'], request.form['stph'], request.form['stemail'], request.form['stcrs'], request.form['clid'], request.form['uname'])
	conn.getlgdata(request.form['uname'], request.form['pwd'], 'student')
	return "Student has been Registered Successfully"

@app.route('/clteachers')
def teacher_manage():
	res = conn.getteacher(session['uname'])
	print(res)
	return render_template('cltrmanage.html', a = res)

@app.route('/clstudents')
def student_manage():
	res = conn.getstudents(session['uname'])
	print(res)
	return render_template('clstmanage.html', a = res)

@app.route('/exmanage')
def exmanage():
	res1 = conn.getcourse()
	res2 = conn.getexam()
	print(res2)
	r1 = []
	for i in res1:
		r1.append((i[0], i[1]))
	return render_template('adexmanage.html', a = r1, b = res2)

@app.route('/declare_exam', methods = ['GET', 'POST'])
def declare_exam():
	conn.createexam(request.form['exname'], request.form['exsdt'], request.form['exedt'], request.form['excrsid'], request.form['exrfee'], request.form['exsem'])
	return "Exam has been declared successfully"

@app.route('/update_exm', methods = ['GET', 'POST'])
def update_exm():
	conn.updateexm(request.form['eid'], request.form['uexname'], request.form['uexsdt'], request.form['uexedt'], request.form['uexcrsid'], request.form['uexrfee'], request.form['uexsem'])
	return "Exam has been updated Successfully"

@app.route('/delete_exm', methods = ['GET', 'POST'])
def delete_exm():
	conn.deleteexm(request.form['eid'])
	return "Exam has been deleted Successfully"

@app.route('/qppmanage')
def qppmanage():
	r = conn.getcourse()
	res = []
	for i in r:
		res.append((i[0], i[1]))
	# fetching exam details one by one
	exms = conn.getexm()
	print('exms', exms)
	e = []
	for i in exms:	
		sect = conn.getqppsect(i[7])
		print('sect',sect)
		e.append((i, sect))
	for i in e:
		print('i',i)
	return render_template('adqppmanage.html', a = res, b = e)

@app.route('/get_exm_crs', methods = ['GET', 'POST'])
def get_exm_crs():
	res = conn.getexmcrs(request.form['eid'])
	r = ""
	for i in res:
		r = r + """<option value="""+str(i[0])+""">"""+str(i[1])+"""</option>"""
	return r

@app.route('/create_qpp', methods = ['GET', 'POST'])
def create_qpp():
	conn.createqpp(request.form['qpexid'], request.form['qptm'],  request.form['qpdurtn'])
	return "Question Paper created successfully"

@app.route('/add_qpp_sect', methods = ['GET', 'POST'])
def add_qpp_sect():
	print(request.form['qppid'], request.form['qpsect'], request.form['qpnoq'], request.form['qpmina'], request.form['qpmpq'], request.form['qpdurtn'])
	conn.addqppsect(request.form['qppid'], request.form['qpsect'], request.form['qpnoq'], request.form['qpmina'], request.form['qpmpq'], request.form['qpdurtn'])
	return "ok"

@app.route('/update_qpsect', methods = ['GET', 'POST'])
def update_qpsect():
	conn.updateqpsect(request.form['qid'], request.form['sect'], request.form['noq'], request.form['mina'], request.form['mpq'], request.form['durn'])
	return "Section updated successfully"

@app.route('/delete_qpsect', methods = ['GET', 'POST'])
def delete_qpsect():
	conn.deleteqpsect(request.form['qid'], request.form['sect'])
	return "Section has been deleted successfully"

@app.route('/qpanmanage')
def qpanamange():
	r = conn.getcourse()
	res = []
	for i in r:
		res.append((i[0], i[1]))
	return render_template('adqpanmanage.html', a = res)

@app.route('/get_sub_sel', methods=['GET', 'POST'])
def get_sub_sel():
	res = conn.getsub(request.form['cid'])
	if res:
		r = """<select name="sub" id="sub" class="form-control" placeholder="Subject" onchange="getpnl(value)">
                        <option disabled="disabled" selected="selected" value="null">Choose Subject
                        </option>"""

		for i in res:
			r = r + """<option value="""+ str(i[0]) +""">"""+ str(i[1]) +"""</option>"""

		r = r + """</select>"""
		return r

@app.route('/get_exm_sel', methods=['GET', 'POST'])
def get_exm_sel():
	res = conn.getxm(request.form['cid'])
	print('ffff',res)
	if res:
		r = """<select name="exam" id="exam" class="form-control" placeholder="Exams">
                        <option disabled="disabled" selected="selected" value="null">Choose Exam
                        </option>"""

		for i in res:
			r = r + """<option value="""+ str(i[0]) +""">"""+ str(i[1]) +"""</option>"""

		r = r + """</select>"""
		return r
	else:
		return "no exams declared for this course"

@app.route('/get_teach_crs', methods = ['GET', 'POST'])
def get_teach_crs():
	res = conn.getteachcrs(request.form['cid'], request.form['eid'], request.form['sid'])
	print( 'in main', res)
	if res:
		r = """<div class="card shadow mb-4">
				<div class="card-header py-3">
				<h6 class="m-0 font-weight-bold text-primary">List of All Teachers</h6>
				</div>
				<div class="card-body">
				<div class="table-responsive">
					<table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
					<thead>
						<tr>
						<th>ID</th>
						<th>Name</th>
						<th>Gender</th>
						<th>College</th>
						<th></th>
						</tr>
					</thead>
					<tbody>"""
		for i in res:
			r = r + """<tr>
						<td>"""+ str(i[0]) +"""</td>
						<td>"""+ str(i[1]) +"""</td>
						<td>"""+ str(i[2]) +"""</td>
						<td>"""+ str(i[13]) +"""</td>
						<td><button class="btn btn-primary" onclick="selteach('"""+ str(i[0]) +"""')">Select</button></td>
						</tr>"""
		r = r + """ </tbody>
					</table>
				</div>
				</div>
			</div>"""
		return r
	else:
		return ""

@app.route('/add_teach_panel', methods =['GET', 'POST'])
def addteachpanel():
	conn.addteachpanel(request.form['tid'], request.form['subid'], request.form['exmid'])
	return "Teacher has been added to panel successfully"

@app.route('/get_teach_panel', methods =['GET', 'POST'])
def get_teach_panel():
	res = conn.getteachpanel(request.form['sid'])
	print(res)
	if res:
		r = """<div class="card shadow mb-4">
				<div class="card-header py-3">
				<h6 class="m-0 font-weight-bold text-primary">List of All Teachers</h6>
				</div>
				<div class="card-body">
				<div class="table-responsive">
					<table class="table table-bordered" id="dataTable" width="100%" cellspacing="0">
					<thead>
						<tr>
						<th>ID</th>
						<th>Name</th>
						<th>Gender</th>
						<th>College</th>
						<th></th>
						</tr>
					</thead>
					<tbody>"""
		for i in res:
			r = r + """<tr>
						<td>"""+ str(i[5]) +"""</td>
						<td>"""+ str(i[6]) +"""</td>
						<td>"""+ str(i[7]) +"""</td>
						<td>"""+ str(i[18]) +"""</td>
						<td><button class="btn btn-danger" onclick="rem('"""+ str(i[0]) +"""')">Remove</button></td>
						</tr>"""
		r = r + """ </tbody>
					</table>
				</div>
				</div>
			</div>"""
		return r
	else:
		return ""

@app.route('/del_teach_panel', methods = ['GET', 'POST'])
def del_teach_panel():
	conn.delteachpanel(request.form['pid'])
	return "Teacher has been removed from the panel successfully"

@app.route('/thqpanel')
def thqpanel():
	res = conn.getpan( session['uname'])
	for i in res:
		print('hello',i)
	return render_template('thqpanmanage.html', a=res)

@app.route('/thqpan_subject', methods = ['GET', 'POST'])
def thqpan_subject():
	res = conn.getqstruct(request.form['eid'], request.form['sid'])
	print('apap',res)
	if res:
		r = """<div class="form-group row">
				<div class="col-sm-6 mb-3 mb-sm-0">
					<select name="qsect" id="qsect" class="form-control" placeholder="Section">
                		<option disabled="disabled" selected="selected" value="null">Choose Section</option>"""

		for i in res:
			r = r + """<option value="""+ str(i[2]) +""">"""+ str(i[2]) +"""</option>"""

		r = r + """</select>
				</div>
				<div class="col-sm-6">
                        <input type="text" name="mdl" id="mdl" class="form-control" placeholder="Module">
                    </div></div>
					<div class="form-group">
						<textarea  name="quest" rows="3" class="form-control" id="quest" placeholder="Question"></textarea>
					</div>
					<div class="form-group">
                   		 <textarea  name="questkey" rows="5" class="form-control" id="questkey" placeholder="Answer Key"></textarea>
                  	</div>"""
		
		return r

@app.route('/thqpan_st', methods = ['GET', 'POST'])
def thqpan_st():
	res = conn.getpn(request.form['eid'], request.form['sid'])
	print(res)
	if res:
		r = """<button class="btn btn-secondary" type="button" data-dismiss="modal">Cancel</button>
            <button class="btn btn-primary" type="button" data-dismiss="modal" onclick="uq('"""+ str(res[0]) +"""')">Submit</button>"""
		return r

@app.route('/up_quest', methods = ['GET', 'POST'])
def up_quest():
	conn.upquest(request.form['pid'], request.form['sect'], request.form['quest'], request.form['key'], session['uname'], request.form['mdl'])
	return "Question has been uploaded to the pool successfully"

@app.route('/updt_sub', methods = ['GET', 'POST'])
def updt_sub():
	conn.updatesubject(request.form['cid'], request.form['usbname'], request.form['usbtype'], request.form['usbsem'], request.form['usbmod'])
	return "Course has been updated successfully"

@app.route('/sylmanage')
def sylmanage():
	r = conn.getcourse()
	res = []
	for i in r:
		res.append((i[0], i[1]))
	print(res)
	return render_template('adsylmanage.html', a = res)

@app.route('/get_sub_select', methods=['GET', 'POST'])
def get_sub_select():
	res = conn.getsub(request.form['cid'])
	if res:
		r = """<select name="sub" id="sub" class="form-control" placeholder="Subject" onchange="getmod(value)">
                        <option disabled="disabled" selected="selected" value="null">Choose Subject
                        </option>"""

		for i in res:
			r = r + """<option value="""+ str(i[0]) +""">"""+ str(i[1]) +"""</option>"""

		r = r + """</select>"""
		return r

@app.route('/get_sub_mno', methods = ['GET', 'POST'])
def get_sub_mno():
	res = conn.getsubmno(request.form['sid'])
	print(res)
	if res:
		r = """<select name="mod" id="mod" class="form-control" placeholder="Module" >
                        <option disabled="disabled" selected="selected" value="null">Choose Module
                        </option>"""

		for i in range(1,res+1):
			r = r + """<option value="""+ str(i) +""">"""+ str(i) +"""</option>"""

		r = r + """</select>"""
		return r

@app.route('/cre_syl', methods = ['GET', 'POST'])
def cre_syl():
	# print(request.form['sid'], request.form['sylmod'], request.form['sylbs'], request.form['wage'])
	conn.cresyl(request.form['sid'], request.form['sylmod'], request.form['sylbs'], request.form['wage'])
	return "Module has been added to the syllabus successfully"

@app.route('/get_syl', methods = ['GET', 'POST'])
def get_syl():
	res = conn.getsyl(request.form['sid'])
	print(res)
	return "ok"

@app.route('/gen_qp', methods = ['GET', 'POST'])
def gen_qp():
	print(request.form['eid'])
	exm = conn.getex(request.form['eid'])
	print(exm)
	qst = conn.getqst(request.form['eid'])
	print(qst)
	sub = conn.getsubjt(exm[0][2],exm[0][3])
	for i in sub:
		print(i)
		syl  = conn.getsyl(i[0])
		for j in syl:
			a = (j[1]/100)*qst[0][3] #converting weightage from percentage to marks
			print('syl', j,a)
			rto = []
			
				

			
				

				# pool = conn.getplq(i[0], k[0], j[0])
				# print(pool)
			
		
		# pool = conn.getplq(i[0])
		# for k in pool:
		# 	print('pool', k)
		
	return render_template('adgenqp.html')

if __name__ == "__main__":
	app.secret_key='my_sessn'
	app.run(debug=True)
