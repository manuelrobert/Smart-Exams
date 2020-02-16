import random
import string
import mysql.connector

con = mysql.connector.connect(host = "localhost", user = "root", passwd = "", database = "db_smart", buffered = True)

def id_generator(chars='SMART'):
	size=5
	num = string.digits
	rst = ''.join(random.choice(num) for _ in range(size))
	return chars + rst

def login(uname, pwd):
	z = con.cursor()
	z.execute("select * from tbl_users where uname='"+ str(uname) +"' and pwd='"+ str(pwd) +"' and status = 1")
	res = z.fetchall()
	return res

def createcourse(cname, cat, strm, typ, durtn, mod):
	z = con.cursor()
	z.execute("insert into tbl_courses values('"+ str(id_generator('CRS')) +"','"+ str(cname) +"','"+ str(cat) +"','"+ str(strm) +"', '"+ str(typ) +"', '"+ str(durtn) +"', '"+ str(mod) +"')")
	con.commit()

def updatecourse(cid, cname, cat, strm, typ, durtn, mod):
	z = con.cursor()
	z.execute("update tbl_courses set crsname='"+ str(cname) +"', crsctgry='"+ str(cat) +"',crsstrm='"+ str(strm) +"', crstype='"+ str(typ) +"', crsdur='"+ str(durtn) +"', crsmod='"+ str(mod) +"' where cid='"+ str(cid) +"' ")
	con.commit()

def deletecourse(cid):
	z = con.cursor()
	z.execute("delete from tbl_courses where cid='"+ str(cid) +"'")
	con.commit()

def getcourse():
	z = con.cursor()
	z.execute("select * from tbl_courses")
	res = z.fetchall()
	return res

def getdcourse(uname):
	z = con.cursor()
	z.execute("select cid, crsname, crsctgry, crsstrm, crstype, crsdur, crsmod from tbl_courses where cid in(select a.crsid from tbl_crsclg a, tbl_colleges b where a.clgid = b.clid and b.uname = '"+ str(uname) +"' )")
	res = z.fetchall()
	return res

def getucourse(uname):
	z = con.cursor()
	z.execute("select cid, crsname, crsctgry, crsstrm, crstype, crsdur, crsmod from tbl_courses where cid not in(select a.crsid from tbl_crsclg a, tbl_colleges b where a.clgid = b.clid and b.uname='"+ str(uname) +"' )")
	res = z.fetchall()
	return res

def createcollege(name, state, dist, city, pin, ph, email, uname):
	z = con.cursor()
	id = id_generator('CLG')
	z.execute("insert into tbl_colleges values('"+ str(id) +"','"+ str(name) +"','"+ str(state) +"','"+ str(dist) +"', '"+ str(city) +"', '"+ str(pin) +"', '"+ str(ph) +"', '"+ str(email) +"', '"+ str(uname) +"')")
	con.commit()

def getlgdata(uname,pwd, utype):
	z = con.cursor()
	z.execute("insert into tbl_users values('"+ str(uname) +"','"+ str(pwd) +"','"+ str(utype) +"', 0)")
	con.commit()

def getcollege():
	z = con.cursor()
	z.execute("select a.clid, a.clname, a.clstate, a.cldist, a.clcity, a.clpin, a.clph, a.clemail, a.uname, b.status from tbl_colleges a, tbl_users b where a.uname=b.uname")
	res = z.fetchall()
	return res

def aprvcolg(uname):
	z = con.cursor()
	z.execute("update tbl_users set status=1 where uname= '"+ str(uname) +"'")
	con.commit()

def daprvcolg(uname):
	z = con.cursor()
	z.execute("update tbl_users set status=0 where uname= '"+ str(uname) +"'")
	con.commit()

def dclrcourse(cid, uname):
	z = con.cursor()
	z.execute("select clid from tbl_colleges where uname = '"+ str(uname) +"'")
	res = z.fetchone()
	z.execute("insert into tbl_crsclg (clgid, crsid) values ('"+ str(res[0]) +"', '"+ str(cid) +"')")
	con.commit()

def getclgcourse(cid):
	z = con.cursor()
	z.execute("select b.cid, b.crsname from tbl_crsclg a, tbl_courses b where a.crsid = b.cid and a.clgid ='"+ str(cid) +"'")
	res = z.fetchall()
	return res

def cresub(cid, sbname, sbtype, sbsem, sbmod):
	z = con.cursor()
	z.execute("insert into tbl_subjects values ('"+ str(id_generator('SBJ')) +"', '"+ str(sbname) +"', '"+ str(sbtype) +"', '"+ str(sbsem) +"', '"+ str(sbmod) +"', '"+ str(cid) +"')")
	con.commit()

def getsub(cid):
	z = con.cursor()
	z.execute("select * from tbl_subjects a, tbl_courses b where a.cid = '"+str(cid)+"' and a.cid = b.cid")
	res = z.fetchall()
	return res

def crssubject(cid):
	z = con.cursor()
	z.execute("select sbid, sbname from tbl_subjects where cid = '"+str(cid)+"'")
	res = z.fetchall()
	return res

def createteacher(trn, trg, trs, trd, trc, trp, trh, tre, trr, trl, tru):
	id = id_generator('THR')
	z = con.cursor()
	z.execute("insert into tbl_teachers values ('"+str(id)+"', '"+str(trn)+"', '"+str(trg)+"', '"+str(trs)+"', '"+str(trd)+"', '"+str(trc)+"', '"+str(trp)+"', '"+str(trh)+"', '"+str(tre)+"', '"+str(trr)+"', '"+str(trl)+"', '"+str(tru)+"')")
	con.commit()

def createstudent(stn, stg, sta, sts, std, stc, stp, sth, ste, sto, stl, stu):
	id = id_generator('STD')
	z = con.cursor()
	z.execute("insert into tbl_students values ('"+str(id)+"', '"+str(stn)+"', '"+str(stg)+"', '"+str(sta)+"', '"+str(sts)+"', '"+str(std)+"', '"+str(stc)+"', '"+str(stp)+"', '"+str(sth)+"', '"+str(ste)+"', '"+str(sto)+"', '"+str(stl)+"', '"+str(stu)+"')")
	con.commit()

def getteacher(uname):
	z = con.cursor()
	z.execute("select a.trid, a.trname, a.trgendr, a.trstate, a.trdist, a.trcity, a.trpin, a.trph, a.tremail, b.status, c.crsname, a.truname from tbl_teachers a, tbl_users b, tbl_courses c, tbl_colleges d where a.truname = b.uname and a.trcid = c.cid and a.trclid = d.clid and d.uname = '"+str(uname)+"'")
	res = z.fetchall()
	return res
	
def getstudents(uname):
	z = con.cursor()
	z.execute("select a.stid, a.stname, a.stgendr, a.stage, a.ststate, a.stdist, a.stcity, a.stpin, a.stph, a.stemail, a.stuname, b.status, c.crsname from tbl_students a, tbl_users b, tbl_courses c, tbl_colleges d where a.stuname = b.uname and a.stcid = c.cid and a.stclid = d.clid and d.uname = '"+str(uname)+"'")
	res = z.fetchall()
	print(res)
	return res

def createexam(exname, exsdt, exedt, excrsid, exrfee, exsem):
	z = con.cursor()
	z.execute("insert into tbl_exams values ('"+str(id_generator('EXM'))+"', '"+str(exname)+"', '"+str(exsdt)+"', '"+str(exedt)+"', '"+str(excrsid)+"', '"+str(exsem)+"', '"+str(exrfee)+"')") 
	con.commit()

def getexam():
	z = con.cursor()
	z.execute("select a.exid, a.exname, a.exsdt, a.exedt, b.crsname, a.exsem, a.regfees, a.excrsid from tbl_exams a, tbl_courses b where a.excrsid = b.cid")
	res = z.fetchall()
	return res

def updateexm(eid, exname, exsdt, exedt, excrsid, exrfee, exsem):
	z = con.cursor()
	z.execute("update tbl_exams set exname = '"+str(exname)+"', exsdt = '"+str(exsdt)+"', exedt = '"+str(exedt)+"', excrsid = '"+str(excrsid)+"', exsem = '"+str(exsem)+"', regfees = '"+str(exrfee)+"' where exid ='"+str(eid)+"'")
	con.commit()

def deleteexm(eid):
	z = con.cursor()
	z.execute("delete from tbl_exams where exid ='"+ str(eid) +"'")
	con.commit()

def getexmcrs(eid):
	z = con.cursor()
	z.execute("select exid, exname, exsem from tbl_exams where excrsid = '"+str(eid)+"'")
	res = z.fetchall()
	return res

def createqpp(eid, tm, durtn):
	z = con.cursor()
	z.execute("insert into tbl_question_papers( qppid, qexmid, qtmarks, qdurtn) values('"+str(id_generator('QPP'))+"', '"+str(eid)+"',  '"+str(tm)+"',  '"+str(durtn)+"')")
	con.commit()

def getqppsect(qpid):
	z = con.cursor()
	z.execute("select  qppart, qpnoq, qpmina, qpmpq, qpdurn from tbl_question_parts  where qppid = '"+str(qpid)+"' ")
	res = z.fetchall()
	return res

def addqppsect(qid, qsect, qnoq, qmina, qmpq, qpdurtn):
	z = con.cursor()
	z.execute("insert into tbl_question_parts (qppid, qppart, qpnoq, qpmina, qpmpq, qpdurn) values('"+str(qid)+"',  '"+str(qsect)+"',  '"+str(qnoq)+"',  '"+str(qmina)+"',  '"+str(qmpq)+"',  '"+str(qpdurtn)+"')")
	con.commit()

def getexm():
	z = con.cursor()
	z.execute("select b.cid, b.crsname,a.exsem, a.exid, a.exname, a.exsdt, a.exedt, c.qppid, c.qtmarks, c.qdurtn  from tbl_exams a, tbl_courses b, tbl_question_papers c where a.excrsid = b.cid and a.exid = c.qexmid")
	res = z.fetchall()
	return res

def updateqpsect(q, s, n, m, p, d):
	z = con.cursor()
	z.execute("update tbl_question_parts set qpnoq ='"+str(n)+"', qpmina ='"+str(m)+"', qpmpq ='"+str(p)+"', qpdurn ='"+str(d)+"' where qppid = '"+str(q)+"' and qppart = '"+str(s)+"' ")
	con.commit()

def deleteqpsect(q, s):
	z = con.cursor()
	z.execute("delete from tbl_question_parts where qppid = '"+str(q)+"' and qppart = '"+str(s)+"' ")
	con.commit()

def getxm(cid):
	z = con.cursor()
	z.execute("select * from tbl_exams where excrsid = '"+str(cid)+"' ")
	res = z.fetchall()
	return res

def getteachcrs(cid, eid, sid):
	z = con.cursor()
	z.execute("select * from tbl_teachers a, tbl_colleges b where a.trcid = '"+str(cid)+"' and a.trclid = b.clid and a.trid not in (select distinct teachid from tbl_question_panels where exmid = '"+ str(eid) +"')")
	res = z.fetchall()
	return res

def addteachpanel(tid, sid, eid):
	z = con.cursor()
	z.execute("insert into tbl_question_panels (plid, subid, exmid, teachid) values ('"+ str(id_generator('PNL')) +"', '"+ str(sid) +"', '"+ str(eid) +"', '"+ str(tid) +"')")
	con.commit()

def getteachpanel(sid):
	z = con.cursor()
	z.execute("select * from tbl_question_panels a, tbl_teachers b, tbl_colleges c where a.subid = '"+str(sid)+"' and a.teachid = b.trid and b.trclid = c.clid")
	res = z.fetchall()
	return res

def delteachpanel(pid):
	z = con.cursor()
	z.execute("delete from tbl_question_panels where id='"+ str(pid) +"'")
	con.commit()

def getpan(uname):
	z = con.cursor()
	z.execute("select d.cid, d.crsname, e.exid, e.exname, f.sbid, f.sbname from tbl_users a, tbl_teachers b, tbl_question_panels c, tbl_courses d, tbl_exams e, tbl_subjects f where a.uname = b.truname and b.trid = c.teachid and c.exmid = e.exid and e.excrsid = d.cid and c.subid = f.sbid and a.uname='"+ str(uname) +"'")
	res = z.fetchall()
	return res

def getqstruct(eid, sid):
	z = con.cursor()
	z.execute("select * from tbl_question_parts a, tbl_question_papers b where a.qppid = b.qppid and b.qexmid = '"+ str(eid) +"'")
	res = z.fetchall()
	return res

def getpn(eid, sid):
	z = con.cursor()
	z.execute("select plid from tbl_question_panels where subid = '"+ str(sid) +"' and exmid = '"+ str(eid) +"'")
	res = z.fetchone()
	return res

def upquest(pid, sect, quest, key, uname, mdl):
	z = con.cursor()
	z.execute("select trid from tbl_teachers where truname = '"+str(uname)+"'")
	res = z.fetchone()
	z.execute("insert into tbl_question_pools values ('"+str(id_generator('QST'))+"', '"+str(pid)+"',  '"+str(res[0])+"',  '"+str(sect)+"',  '"+str(quest)+"',  '"+str(key)+"',  '"+str(mdl)+"')")
	con.commit()

def updatesubject(sid, snm, stp, sem, smd):
	z = con.cursor()
	z.execute("update tbl_subjects set sbname = '"+str(snm)+"', sbtype = '"+str(stp)+"', sem = '"+str(sem)+"', nomod = '"+str(smd)+"' where sbid = '"+str(sid)+"'")
	con.commit()

def getsubmno(sid):
	z = con.cursor()
	z.execute("select nomod from tbl_subjects where sbid = '"+str(sid)+"'")
	res = z.fetchone()
	return res[0]

def cresyl(sid, mod, sbs, wage):
	z = con.cursor()
	z.execute("insert into tbl_syllabus (sylsub, sylmod, syllabus,weight) values ('"+str(sid)+"', '"+str(mod)+"', '"+str(sbs)+"', '"+str(wage)+"')")
	con.commit()

def getsyl(sid):
	z = con.cursor()
	z.execute("select sylmod, weight from tbl_syllabus where sylsub = '"+str(sid)+"'")
	res = z.fetchall()
	return res

def getex(eid):
	z = con.cursor()
	z.execute("select a.exid, a.exname, a.exsem, b.cid, b.crsname, b.crsctgry from tbl_exams a, tbl_courses b where exid = '"+str(eid)+"' and a.excrsid = b.cid")
	res = z.fetchall()
	return res

def getsubjt(sem, cid):
	z = con.cursor()
	z.execute("select sbid, sbname, sbtype, sem, nomod from tbl_subjects where cid ='"+str(cid)+"' and sem = '"+str(sem)+"'")
	res = z.fetchall()
	return res

def getplq(sid, sect, md):
	z = con.cursor()
	z.execute("select a.plid, b.qid from tbl_question_panels a, tbl_question_pools b where a.subid = '"+str(sid)+"' and b.qsect ='"+str(sect)+"' and b.qsmod = '"+str(md)+"' and a.plid = b.qplid")
	res = z.fetchall()
	return res

def getqst(eid):
	z = con.cursor()
	z.execute("select a.qppart, a.qpmina, a.qpmpq, b.qtmarks from tbl_question_parts a, tbl_question_papers b where a.qppid = b.qppid and b.qexmid = '"+str(eid)+"' ")
	res = z.fetchall()
	return res

def getinpqst(eid, sid, sectid, mod):
	print('ins', eid, sid, sectid, mod)	
	z = con.cursor()
	z.execute("select b.qid, b.quest from tbl_question_panels a, tbl_question_pools b where a.exmid = '"+str(eid)+"' and a.subid = '"+str(sid)+"' and a.plid = b.qplid and b.qsect = '"+str(sectid)+"' and b.qsmod = '"+str(mod)+"'")
	res = z.fetchall()
	return res

def insqst(eid, cid, sid, sectid, qid):
	print('get', eid, cid, sid, sectid, qid)
	z = con.cursor()
	z.execute("insert into tbl_gen_qp values('"+ str(id_generator('QPR')) +"','"+ str(eid) +"', '"+ str(cid) +"', '"+ str(sid) +"', '"+ str(sectid) +"','"+ str(qid) +"')")
	con.commit()

def delqp(eid, cid):
	z = con.cursor()
	z.execute("delete from tbl_gen_qp where eid = '"+ str(eid) +"' and cid = '"+ str(cid) +"' ")
	con.commit()

def tempexm(eid, cid):
	res  = []
	z = con.cursor()
	z.execute("select b.cid, b.crsname, a.exname, a.exsem from tbl_exams a, tbl_courses b where a.exid = '"+ str(eid) +"' and a.excrsid = b.cid")
	crs = z.fetchall()
	res.append((eid, crs[0][2], crs[0][0], crs[0][1], crs[0][3]))
	return res

def getquestionpaper(eid, cid):
	res  = []
	z = con.cursor()
	z.execute("select b.cid, b.crsname, a.exname, a.exsem from tbl_exams a, tbl_courses b where a.exid = '"+ str(eid) +"' and a.excrsid = b.cid")
	crs = z.fetchall()
	z.execute("select qppid, qtmarks, qdurtn from tbl_question_papers where qexmid = '"+ str(eid) +"'")
	qp = z.fetchall()
	z.execute("select qppart, qpmina, qpmpq, qpdurn from tbl_question_parts where qppid = '"+ str(qp[0][0]) +"'")
	qpt = z.fetchall()
	print('crs',crs)
	print( 'qp', qp)
	print( 'qpt', qpt)
	z.execute("select sbid, sbname from tbl_subjects where cid = '"+ str(cid)+"'")
	sbj = z.fetchall()
	# res.append((eid, crs[0][2], crs[0][0], crs[0][1], crs[0][3]))
	for i in sbj:
		print(i)
		z.execute("select plid from tbl_question_panels where subid ='"+ str(i[0]) +"'  and exmid = '"+ str(eid) +"'")
		pl = z.fetchone()
		if pl:
			x = []
			y = []
			# res.append((i[0],i[1]))
			x.append((i[0],i[1], qp[0][1], qp[0][2]))
			print('pnl', pl[0])
			z.execute("select b.qid, b.qsect, b.quest from tbl_gen_qp a, tbl_question_pools b where a.eid = '"+ str(eid) +"' and a.cid = '"+ str(cid)+"' and a.sid = '"+ str(i[0]) +"' and a.qid = b.qid and b.qplid = '"+ str(pl[0])+"'")
			qst = z.fetchall()
			print(qst)
			x.append((qpt))
			for j in qst:
				for k in qpt:
					if j[1] == k[0]:
						# res.append((k[0], k[1], k[2], k[3], j[0], j[1], j[2]))
						y.append((j[0], j[1], j[2]))
			res.append((x, y))
	print(res)
	return res

def getexamcl(uname):
	z = con.cursor()
	z.execute("select c.exid, c.exname, c.exsem from tbl_colleges a, tbl_crsclg b, tbl_exams c where a.uname = '"+ str(uname) +"' and a.clid = b.clgid and b.crsid = c.excrsid")
	res = z.fetchall()
	print(res)
	return res

def getsubexm(eid):
	z = con.cursor()
	z.execute("select b.sbid, b.sbname from tbl_exams a, tbl_subjects b where a.exid = '"+ str(eid) +"' and a.excrsid = b.cid and a.exsem = b.sem")
	res = z.fetchall()
	return res

def getquestppr(eid, sid):
	z = con.cursor()
	z.execute("select a.qid, a.sect, b.quest from tbl_gen_qp a, tbl_question_pools b where a.eid = '"+ str(eid) +"' and a.sid = '"+ str(sid) +"' and a.qid = b.qid")
	res1 = z.fetchall()
	z.execute("select b.qppart, b.qpnoq, b.qpmina, b.qpmpq,b.qpdurn from tbl_question_papers a, tbl_question_parts b where a.qexmid = '"+ str(eid) +"' and a.qppid = b.qppid")	
	res2 = z.fetchall()
	z.execute("select * from tbl_question_papers where qexmid = '"+ str(eid) +"'")
	res3 = z.fetchall()
	z.execute("select stid from tbl_exregister where exmid = '"+ str(eid) +"'")
	res4 = z.fetchall()
	res5 = []
	res5.append((res3, res4, res2, res1))
	return res5

def getexamst(uname):
	z = con.cursor()
	z.execute("select b.exid, b.exname, b.exsdt, b.exedt, b.exsem, b.regfees from tbl_students a, tbl_exams b where  a.stuname ='"+ str(uname) +"' and a.stcid = b.excrsid")
	res = z.fetchall()
	return res

def regexam(eid, uname):
	z = con.cursor()
	z.execute("select stid from tbl_students where stuname = '"+ str(uname) +"'")
	res = z.fetchone()
	z.execute("insert into tbl_exregister (exmid, stid) values ('"+ str(eid) +"', '"+ str(res[0]) +"')")
	con.commit()

def uplanswer(e, s, st, sct, qid, f):
	print(e, s, st, sct, qid, f)
	z = con.cursor()
	z.execute("insert into tbl_answers values('"+ str(id_generator('ANS')) +"','"+ str(e) +"','"+ str(s) +"','"+ str(sct) +"', '"+ str(qid) +"', '"+ str(f) +"', '"+ str(st) +"')")
	con.commit()

def checkes(eid, uname):
	z = con.cursor()
	z.execute("select stid from tbl_students where stuname = '"+ str(uname) +"'")
	res = z.fetchone()
	z.execute("select * from tbl_exregister where exmid = '"+ str(eid) +"' and stid = '"+ str(res[0]) +"' ")
	r = z.fetchall()
	return r

def getexmv():
	z = con.cursor()
	z.execute("select distinct a.exid, a.exname, a.excrsid, b.crsname, a.exsem from tbl_exams a, tbl_courses b, tbl_answers c where  a.excrsid = b.cid and a.exid = c.exid")
	res = z.fetchall()
	return res

def getec(eid):
	z = con.cursor()
	z.execute("select exid, excrsid from tbl_exams a where exid = '"+ str(eid) +"'")
	res = z.fetchall()
	return res

def getqppr(eid):
	z = con.cursor()
	z.execute("select qppid, qtmarks, qdurtn from tbl_question_papers where qexmid = '"+ str(eid) +"'")
	res = z.fetchall()
	return res

def getqppt(q):
	z = con.cursor()
	z.execute("select qppart, qpnoq, qpmina, qpmpq, qpdurn from tbl_question_parts where qppid = '"+ str(q) +"'")
	res = z.fetchall()
	return res

def getstrnex(eid):
	z = con.cursor()
	z.execute("select stid from tbl_exregister where exmid = '"+ str(eid) +"' ")
	res = z.fetchall()
	return res

def getsubcr(crs):
	z = con.cursor()
	z.execute("select sbid from tbl_subjects where cid = '"+ str(crs) +"'")
	res  = z.fetchall()
	return res

def getqstp(s, e, c):
	z = con.cursor()
	z.execute("select sect, qid  from tbl_gen_qp where eid = '"+ str(e) +"' and cid = '"+ str(c) +"' and sid = '"+ str(s) +"' order by sect")
	res = z.fetchall()
	return res

def getansstd(e, s, sect, q, strn):
	z = con.cursor()
	z.execute("select file from tbl_answers where exid ='"+ str(e) +"' and subid = '"+ str(s) +"' and sectid = '"+ str(sect) +"' and qid = '"+ str(q) +"' and stid = '"+ str(strn) +"'")
	res = z.fetchall()
	return res

def getanskey(qst):
	z = con.cursor()
	z.execute("select qkey from tbl_question_pools where qid = '"+ str(qst) +"'")
	res = z.fetchall()
	return res