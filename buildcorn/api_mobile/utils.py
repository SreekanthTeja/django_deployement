from rest_framework import serializers, status
from buildcorn.models import Report, AnswerChecklist, Project
def generate_report(**kwargs):
    if kwargs['typee'] == 'Quality':
        try:
            project = Project.objects.get(name__exact=kwargs['project'])
            rep, created = Report.objects.get_or_create(typee=kwargs['typee'],project=kwargs['project'],name=kwargs['checklist'], submitted_by=kwargs['submitted_by'],)
            
            total_ans_obj_count = AnswerChecklist.objects.filter(quality_checklist__name=kwargs.get('checklist',None),question__typee=kwargs['typee']).count()
            ans_obj_status_count = AnswerChecklist.objects.filter(quality_checklist__name=kwargs.get('checklist',None),question__typee=kwargs['typee'],status=AnswerChecklist.COMPILED).count()
            print("?????",total_ans_obj_count,ans_obj_status_count )
            if created and  (total_ans_obj_count == ans_obj_status_count):
                rep.status = Report.DONE
                rep.save()
                project.inspection = Project.INSPECTION_DONE
                project.save()
            elif ans_obj_status_count < total_ans_obj_count:
                rep.status = Report.PENDING
                rep.save()
            else:
                rep.status = Report.DONE
                rep.save()
                project.inspection = Project.INSPECTION_DONE
                project.save()
        except Exception as e:
            raise serializers.ValidationError({'error':e},)
    else:
        try:
            rep, created = Report.objects.get_or_create(typee=kwargs['typee'],project=kwargs['project'],name=kwargs['checklist'], submitted_by=kwargs['submitted_by'],)
            
            total_ans_obj_count = AnswerChecklist.objects.filter(safety_checklist__name=kwargs.get('checklist',None),question__typee=kwargs['typee']).count()
            ans_obj_status_count = AnswerChecklist.objects.filter(safety_checklist__name=kwargs.get('checklist',None),question__typee=kwargs['typee'],status=AnswerChecklist.COMPILED).count()
            print("?????",total_ans_obj_count,ans_obj_status_count )
            if created and  (total_ans_obj_count == ans_obj_status_count):
                rep.status = Report.DONE
                rep.save()
                project.inspection = Project.INSPECTION_DONE
                project.save()
            elif ans_obj_status_count < total_ans_obj_count:
                rep.status = Report.PENDING
                rep.save()
            else:
                rep.status = Report.DONE
                rep.save()
                project.inspection = Project.INSPECTION_DONE
                project.save()
        except Exception as e:
            raise serializers.ValidationError({'error':e}, status=status.HTTP_400_BAD_REQUEST)
