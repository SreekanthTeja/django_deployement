from rest_framework import serializers, status
from buildcorn.models import Report, AnswerChecklist, Project, Employee, Approver
from accounts.models import Company
import json
from django.core.files.storage import FileSystemStorage
import datetime
from django.conf import settings
import os
from base64 import b64decode
from django.contrib.auth import get_user_model
from dashboard.models import ChecklistsUsage
User = get_user_model()
def pdf_file(pdf):
    print(pdf)
    location = '%s/report'%(settings.MEDIA_ROOT)
    try:
        fs = FileSystemStorage(location=location)
        picname = "REPORT_%s.pdf"%(datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f'))
        f_save = fs.save(picname, pdf)
        filepath = "%s/%s"%(location,picname)
    except Exception as e:
        raise serializers.ValidationError({"error":e})
    # return json.dumps(filepath)
    return filepath

def approver_action(data,employee,checklist_name):
    try:
        project = Project.objects.get(name=data["project"],employee__user__email=employee)
        checklist_usage_obj, created = ChecklistsUsage.objects.get_or_create(project=project,company=project.company,name=checklist_name,typee=data["type"])
        if created:
            checklist_usage_obj.count +=1
            checklist_usage_obj.save()
        if not created:
            checklist_usage_obj.count +=1
            checklist_usage_obj.save()
        complied = [True for question in data["question"]  if (question["reason"] == None) or (question["reason"] == "")]
        if complied:
            approver = User.objects.get(email=project.approver)
            employee = Employee.objects.get(user__email=employee)
            approver_obj, created = Approver.objects.get_or_create(user=approver, project=project,submitted_employee= employee)
            # report = pdf_file(report)
            # data["report"]= report
            if created:
                
                approver_obj.data =json.dumps(data)
                approver_obj.save()
            else:
                approver_obj.data =json.dumps(data)
                approver_obj.save()
    except Exception as e:
        raise serializers.ValidationError({"error":e})
        
        

def pdf_file(pdf):
    bytess = b64decode(pdf, validate=True)
    # if bytess[0:4] != b'%PDF':
    #     raise serializers.ValidationError({'error':'Missing the PDF file signature'})
    location = '%s/report'%(settings.MEDIA_ROOT)
    try:
        filename = "REPORT_%s.pdf"%(datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f'))
        filepath = "%s/%s"%(location,filename)
        f = open(filepath, 'wb')
        f.write(bytess)
        f.close()
    except Exception as e:
        raise serializers.ValidationError({"error":e})
    return json.dumps(filepath)

def generate_report(**kwargs):
    emp = Employee.objects.get(user__first_name=kwargs['submitted_by'])
    project = Project.objects.get(name__exact=kwargs['project'],employee__in=[emp.id], company=emp.company)
    if kwargs['typee'] == 'Quality':
        try:
            rep, created = Report.objects.get_or_create(company=emp.company,typee=kwargs['typee'],project=project,name=kwargs['checklist'], submitted_by=kwargs['submitted_by'],)

            total_ans_obj_count = AnswerChecklist.objects.filter(quality_checklist__name=kwargs.get('checklist',None),question__typee=kwargs['typee']).count()
            ans_obj_status_count = AnswerChecklist.objects.filter(quality_checklist__name=kwargs.get('checklist',None),question__typee=kwargs['typee'],status=AnswerChecklist.COMPILED).count()
            print("?????",total_ans_obj_count,ans_obj_status_count )
            if created and  (total_ans_obj_count == ans_obj_status_count):
                rep.status = Report.DONE
                rep.download = json.loads(kwargs["pdf"])
                rep.save()
                project.inspection = Project.INSPECTION_DONE
                project.save()
            elif ans_obj_status_count < total_ans_obj_count:
                rep.status = Report.PENDING
                rep.download = json.loads(kwargs["pdf"])
                rep.save()
            else:
                rep.status = Report.DONE
                rep.save()
                rep.download = json.loads(kwargs["pdf"])
                project.inspection = Project.INSPECTION_DONE
                project.save()
        except Exception as e:
            raise serializers.ValidationError({'error':e},)
    else:
        try:
            rep, created = Report.objects.get_or_create(company=emp.company,typee=kwargs['typee'],project=project,name=kwargs['checklist'], submitted_by=kwargs['submitted_by'],)

            total_ans_obj_count = AnswerChecklist.objects.filter(safety_checklist__name=kwargs.get('checklist',None),question__typee=kwargs['typee']).count()
            ans_obj_status_count = AnswerChecklist.objects.filter(safety_checklist__name=kwargs.get('checklist',None),question__typee=kwargs['typee'],status=AnswerChecklist.COMPILED).count()
            print("safety....",total_ans_obj_count,ans_obj_status_count, kwargs["pdf"])
            if created and  (total_ans_obj_count == ans_obj_status_count):
                rep.status = Report.DONE
                rep.download = json.loads(kwargs["pdf"])
                rep.save()
                project.inspection = Project.INSPECTION_DONE
                project.save()
            elif ans_obj_status_count < total_ans_obj_count:
                rep.status = Report.PENDING
                rep.download = json.loads(kwargs["pdf"])
                rep.save()
            else:
                rep.status = Report.DONE
                rep.download = json.loads(kwargs["pdf"])
                rep.save()
                project.inspection = Project.INSPECTION_DONE
                project.save()
        except Exception as e:
            raise serializers.ValidationError({'error':e})




        # print("report:",request.data.get('report'), type(request.data.get('report')))
        # f = request.data.get('report')
        # input_data = {
        #     "project":"Logos",
        #     "type":"Safety",
        #     "question": [
        #         {
        #             "id": 20,
        #             "question": "Why safety",
        #             "status": "Complied",
        #             "reason": None

        #         }
        #     ]
        # }
        # filee = request.FILES.get('report', None)
        # input_data["report"] = filee
        
        # pdf = pdf_file(filee) if filee != None else "empty"