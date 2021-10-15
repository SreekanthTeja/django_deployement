# from rest_framework import serializers, status
# from buildcorn.models import Report, AnswerChecklist, Project, Employee, Approver
# from accounts.models import Company
# import json
# from django.core.files.storage import FileSystemStorage
# import datetime
# from django.conf import settings
# import os
# from base64 import b64decode
# from django.contrib.auth import get_user_model
# User = get_user_model()
# def pdf_file(pdf):
#     bytess = b64decode(pdf, validate=True)
#     # if bytess[0:4] != b'%PDF':
#     #     raise serializers.ValidationError({'error':'Missing the PDF file signature'})
#     location = '%s/report'%(settings.MEDIA_ROOT)
#     try:
#         filename = "REPORT_%s.pdf"%(datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f'))
#         filepath = "%s/%s"%(location,filename)
#         f = open(filepath, 'wb')
#         f.write(bytess)
#         f.close()
#     except Exception as e:
#         raise serializers.ValidationError({"error":e})
#     return json.dumps(filepath)

# def generate_report(**kwargs):
#     emp = Employee.objects.get(user__first_name=kwargs['submitted_by'])
#     project = Project.objects.get(name__exact=kwargs['project'],employee__in=[emp.id], company=emp.company)
#     if kwargs['typee'] == 'Quality':
#         try:
#             rep, created = Report.objects.get_or_create(company=emp.company,typee=kwargs['typee'],project=project,name=kwargs['checklist'], submitted_by=kwargs['submitted_by'],)

#             total_ans_obj_count = AnswerChecklist.objects.filter(quality_checklist__name=kwargs.get('checklist',None),question__typee=kwargs['typee']).count()
#             ans_obj_status_count = AnswerChecklist.objects.filter(quality_checklist__name=kwargs.get('checklist',None),question__typee=kwargs['typee'],status=AnswerChecklist.COMPILED).count()
#             print("?????",total_ans_obj_count,ans_obj_status_count )
#             if created and  (total_ans_obj_count == ans_obj_status_count):
#                 rep.status = Report.DONE
#                 rep.download = json.loads(kwargs["pdf"])
#                 rep.save()
#                 project.inspection = Project.INSPECTION_DONE
#                 project.save()
#             elif ans_obj_status_count < total_ans_obj_count:
#                 rep.status = Report.PENDING
#                 rep.download = json.loads(kwargs["pdf"])
#                 rep.save()
#             else:
#                 rep.status = Report.DONE
#                 rep.save()
#                 rep.download = json.loads(kwargs["pdf"])
#                 project.inspection = Project.INSPECTION_DONE
#                 project.save()
#         except Exception as e:
#             raise serializers.ValidationError({'error':e},)
#     else:
#         try:
#             rep, created = Report.objects.get_or_create(company=emp.company,typee=kwargs['typee'],project=project,name=kwargs['checklist'], submitted_by=kwargs['submitted_by'],)

#             total_ans_obj_count = AnswerChecklist.objects.filter(safety_checklist__name=kwargs.get('checklist',None),question__typee=kwargs['typee']).count()
#             ans_obj_status_count = AnswerChecklist.objects.filter(safety_checklist__name=kwargs.get('checklist',None),question__typee=kwargs['typee'],status=AnswerChecklist.COMPILED).count()
#             print("safety....",total_ans_obj_count,ans_obj_status_count, kwargs["pdf"])
#             if created and  (total_ans_obj_count == ans_obj_status_count):
#                 rep.status = Report.DONE
#                 rep.download = json.loads(kwargs["pdf"])
#                 rep.save()
#                 project.inspection = Project.INSPECTION_DONE
#                 project.save()
#             elif ans_obj_status_count < total_ans_obj_count:
#                 rep.status = Report.PENDING
#                 rep.download = json.loads(kwargs["pdf"])
#                 rep.save()
#             else:
#                 rep.status = Report.DONE
#                 rep.download = json.loads(kwargs["pdf"])
#                 rep.save()
#                 project.inspection = Project.INSPECTION_DONE
#                 project.save()
#         except Exception as e:
#             raise serializers.ValidationError({'error':e})

def generate_report(sender, instance, **kwargs):
    if (kwargs["created"] == False ) and (instance.is_approved == True):
        # print("generate report",) 
        pass
    pass