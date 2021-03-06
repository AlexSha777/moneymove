from django import forms
from django.utils import timezone, dateformat
from django.forms import ModelForm
from .models import Income, Spendings, MoneySource, SpendingKind, Cash, CashKind

from datetime import datetime, date, time

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _    




class AddIncome(ModelForm):
    

    class Meta:
        model = Income
        fields = ['date_field', 'source', 'ammount', 'cash_kind_income', 'comment']

        labels = {
                'date_field': _('Дата'),
                'source': _('Доход'),
                'ammount': _('Сумма'),
                'cash_kind_income': _('Пополняемые имеющиеся средства'),
                'comment': _('Комментарий')
        }
    
   



    def clean_date_field(self):
        
        data_valid = self.cleaned_data['date_field']
        
        if str(data_valid) > dateformat.format(timezone.now(), 'Y-m-d'):
            raise ValidationError(_('Invalid date - it is in future'))

        
        return data_valid

    def clean_source(self):
                
        source_valid = self.cleaned_data['source']
        
        if source_valid not in [p for p in MoneySource.objects.all()]:
            raise ValidationError(_('Invalid date - not in income source list'))

        return source_valid

    def clean_ammount(self):
              
        ammount_valid = self.cleaned_data['ammount']
        if ammount_valid <= 0:
            raise ValidationError(_('Invalid date - ammount can not be less than 0'))

        return ammount_valid

    def clean_cash_kind_income(self):
                
        cash_kind_income_valid = self.cleaned_data['cash_kind_income']
        
        if cash_kind_income_valid not in [p for p in CashKind.objects.all()]:
            raise ValidationError(_('Invalid cash kind - not in Cash Kind list'))

        return cash_kind_income_valid

    def clean_comment(self):
        
        comment_valid = self.cleaned_data['comment']
        if len(comment_valid)>150:
            raise ValidationError(_('Invalid date - comment is too long'))
        
        return comment_valid

class AddMoneySource(forms.Form):

    first_level_source = forms.CharField(label = 'Основной раздел')
    second_level_source = forms.CharField(label = 'Детализация')

    
    def clean_first_level_source(self):
                
        first_level_source_valid = self.cleaned_data['first_level_source']
        
        first_level_source_valid = str.lower(first_level_source_valid)
        first_level_source_valid = str.capitalize(first_level_source_valid)

        
        return first_level_source_valid

    def clean_second_level_source(self):
                
        second_level_source_valid = self.cleaned_data['second_level_source']
        

        
        first_level = self.cleaned_data['first_level_source']
        
        second_level_source_valid = str.capitalize(second_level_source_valid)

        if str.lower(self.cleaned_data['first_level_source']) in [str.lower(p.first_level_source) for p in MoneySource.objects.all()]:
            
            personal_second_level = [str.lower(p.second_level_source) for p in MoneySource.objects.all().filter(first_level_source=first_level)]

                    
            if str.lower(second_level_source_valid) in personal_second_level:
                
                raise ValidationError(_('Invalid date - source is aiready exist'))

        

        return second_level_source_valid


class AddSpendingKind(forms.Form):

    first_level_kind = forms.CharField(label = 'Основной раздел')
    second_level_kind = forms.CharField(label = 'Детализация')

    
    def clean_first_level_kind(self):
                
        first_level_kind_valid = self.cleaned_data['first_level_kind']
        
        first_level_kind_valid = str.lower(first_level_kind_valid)
        first_level_kind_valid = str.capitalize(first_level_kind_valid)

        
        return first_level_kind_valid

    def clean_second_level_kind(self):
                
        second_level_kind_valid = self.cleaned_data['second_level_kind']
        

        
        first_level = self.cleaned_data['first_level_kind']
        
        second_level_kind_valid = str.lower(second_level_kind_valid)
        second_level_kind_valid = str.capitalize(second_level_kind_valid)

        if self.cleaned_data['first_level_kind'] in [p.first_level_kind for p in SpendingKind.objects.all()]:
            
            personal_second_level = [p.second_level_kind for p in SpendingKind.objects.all().filter(first_level_kind=first_level)]

                    
            if second_level_kind_valid in personal_second_level:
                
                raise ValidationError(_('Invalid date - source is aiready exist'))

        

        return second_level_kind_valid



class AddSpendings(forms.Form):
    

    spendings_kind_objects = SpendingKind.objects.all()
    blank_choice = ('', '---Введите значение---')
    first_level_kind_unique = []
    
    if spendings_kind_objects:
    	for p in spendings_kind_objects:
    		if p.first_level_kind not in first_level_kind_unique:
                first_level_kind_unique.append(p.first_level_kind)

    second_level_kind_unique = []
    
    if spendings_kind_objects:
        for p in spendings_kind_objects:
            if p.second_level_kind not in first_level_kind_unique:
                second_level_kind_unique.append(p.second_level_kind)


        
    first_level_kind_unique_tuple = []
    second_level_kind_unique_tuple = []


    increment = 0
    for i in first_level_kind_unique:
        increment +=1
        to_add = [i, i]
        to_add = tuple(to_add)
        first_level_kind_unique_tuple.append(to_add)
        
    first_level_kind_unique_tuple.append(blank_choice)
    first_level_kind_unique_tuple = tuple(first_level_kind_unique_tuple)
    
        
    increment_1 = 0
    for i in second_level_kind_unique:
        increment_1 +=1
        to_add = [i, i]
        to_add = tuple(to_add)
        second_level_kind_unique_tuple.append(to_add)

    second_level_kind_unique_tuple.append(blank_choice)
    second_level_kind_unique_tuple = tuple(second_level_kind_unique_tuple)

    cash_kind_tuple = [(p.id, str(p)) for p in CashKind.objects.all()]
    
    cash_kind_tuple.append(blank_choice)
    

    date_field = forms.DateField(label ='Дата')   
    first_level_kind = forms.TypedChoiceField(label = 'Вид расхода Основной', choices=first_level_kind_unique_tuple,  coerce = str)
    second_level_kind = forms.TypedChoiceField(label = 'Вид расхода Детализация',choices=second_level_kind_unique_tuple, coerce = str)
    ammount = forms.FloatField(label ='Сумма', help_text="000.00")
    cash_kind_spending = forms.TypedChoiceField(label = 'Источник расходуемых имеющихся средств', choices=cash_kind_tuple,  coerce = str)
    comment = forms.CharField(label ='Комментарий', help_text="Any comments?")

    
    def get_first_level_kind_unique_tuple(self):
        
        spendings_kind_objects = SpendingKind.objects.all()
        first_level_kind_unique = [p.first_level_kind for p in spendings_kind_objects]

        first_level_kind_unique_tuple = []
        increment = 0
        for i in first_level_kind_unique:
            increment +=1
            to_add = [increment, i]
            to_add = tuple(to_add)
            first_level_kind_unique_tuple.append(to_add)
        
        first_level_kind_unique_tuple = tuple(first_level_kind_unique_tuple)
        
        return self.first_level_kind_unique_tuple
    

    def get_second_level_kind_unique_tuple(self):
        
        spendings_kind_objects = SpendingKind.objects.all()
        second_level_kind_unique = [p.second_level_kind for p in spendings_kind_objects]
        second_level_kind_unique_tuple = []

        increment_1 = 0
        for i in second_level_kind_unique:
            increment_1 +=1
            to_add = [increment_1, i]
            to_add = tuple(to_add)
            second_level_kind_unique_tuple.append(to_add)


        second_level_kind_unique_tuple = tuple(second_level_kind_unique_tuple)

        

        return self.second_level_kind_unique_tuple

    


    def clean_date_field(self):
        
        data_valid = self.cleaned_data['date_field']

        
        # Check if a date is not in the past. 
        if str(data_valid) < dateformat.format(timezone.now(), 'Y-m-d'):
            raise ValidationError(_('Invalid date - date is in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if str(data_valid) > dateformat.format(timezone.now(), 'Y-m-d'):
            raise ValidationError(_('Invalid date - it is in future'))

       
        # Remember to always return the cleaned data.
        return data_valid


    def clean_first_level_kind(self):
        
        

        first_level_kind_valid = self.cleaned_data['first_level_kind']
        
        
        spendings_kind_objects = SpendingKind.objects.all()

        if first_level_kind_valid not in [p.first_level_kind for p in spendings_kind_objects]:
            raise ValidationError(_('Invalid data - not in spendings kind 1 level list'))

        
        return first_level_kind_valid

    def clean_second_level_kind(self):
        
        second_level_kind_valid = self.cleaned_data['second_level_kind']
        
        spendings_kind_objects = SpendingKind.objects.all()
                
        if second_level_kind_valid not in [p.second_level_kind for p in spendings_kind_objects]:
            
            raise ValidationError(_('Invalid data - not in spendings kind 2 level list'))

                
        first_level_kind_generic = self.cleaned_data['first_level_kind']
        
        personal_number_second_level_kind = [p.second_level_kind for p in SpendingKind.objects.all().filter(first_level_kind=first_level_kind_generic)]

        if second_level_kind_valid not in personal_number_second_level_kind:
            
            raise ValidationError(_('Invalid data - not in spendings kind 2 with 1 level data'))
        
        return second_level_kind_valid

    
    def clean_ammount(self):
        
        ammount_valid = self.cleaned_data['ammount']
                
        if ammount_valid <= 0:
            raise ValidationError(_('Invalid data - ammount can not be less than 0'))

        return ammount_valid
    
    
    def clean_comment(self):
             
        comment_valid = self.cleaned_data['comment']

        if len(comment_valid)>150:
            raise ValidationError(_('Invalid data - comment is too long'))

        return comment_valid

class AddCash(ModelForm):
    

    class Meta:
        model = Cash
        fields = ['date_field', 'cash_kind', 'ammount', 'purpose', 'comment']

        labels = {
                'date_field': _('Дата'),
                'cash_kind': _('Вид средств'),
                'ammount': _('Сумма'),
                'purpose': _('Инициализация приложения'),
                'comment': _('Комментарий')
        }
    
    def clean_date_field(self):
        
        data_valid = self.cleaned_data['date_field']
        if str(data_valid) < dateformat.format(timezone.now(), 'Y-m-d'):
            raise ValidationError(_('Invalid date - date is in past'))

        if str(data_valid) > dateformat.format(timezone.now(), 'Y-m-d'):
            raise ValidationError(_('Invalid date - it is in future'))

        
        return data_valid

    def clean_cash_kind(self):
                
        cash_kind_valid = self.cleaned_data['cash_kind']
        
        if cash_kind_valid not in [p for p in CashKind.objects.all()]:
            raise ValidationError(_('Invalid date - not in cash kind list'))

        return cash_kind_valid

    def clean_ammount(self):
              
        ammount_valid = self.cleaned_data['ammount']
        if ammount_valid <= 0:
            raise ValidationError(_('Invalid date - ammont can not be less than 0'))

        return ammount_valid

    def clean_comment(self):
        
        comment_valid = self.cleaned_data['comment']
        if len(comment_valid)>150:
            raise ValidationError(_('Invalid date - comment is too long'))
        
        return comment_valid


class AddCashKind(forms.Form):

    first_level_cashkind = forms.CharField(label = 'Основной раздел')
    second_level_cashkind = forms.CharField(label = 'Детализация')

    
    def clean_first_level_cashkind(self):
                
        first_level_cashkind_valid = self.cleaned_data['first_level_cashkind']
        
        first_level_cashkind_valid = str.lower(first_level_cashkind_valid)
        first_level_cashkind_valid = str.capitalize(first_level_cashkind_valid)

        
        return first_level_cashkind_valid

    def clean_second_level_cashkind(self):
                
        second_level_cashkind_valid = self.cleaned_data['second_level_cashkind']
        

        
        first_level = self.cleaned_data['first_level_cashkind']
        
        
        second_level_cashkind_valid = str.capitalize(second_level_cashkind_valid)

        if str.lower(self.cleaned_data['first_level_cashkind']) in [str.lower(p.first_level_cashkind) for p in CashKind.objects.all()]:
            
            personal_second_level = [str.lower(p.second_level_cashkind) for p in CashKind.objects.all().filter(first_level_cashkind=first_level)]

                    
            if str.lower(second_level_cashkind_valid) in personal_second_level:
                
                raise ValidationError(_('Неверная детализация - запись уже существует'))

        return second_level_cashkind_valid

class Analysing(forms.Form):
    
    analysing_main_tuple = []
    unique_list_main = ['Доходы', 'Расходы', 'Имеющиеся средства']

    for i in unique_list_main:
        
        to_add = [i, i]
        to_add = tuple(to_add)
        analysing_main_tuple.append(to_add)

    analysing_main_tuple = tuple(analysing_main_tuple)
  
    
    analysing_main_first_level_tuple = []
    unique_list_main = ['Доходы', 'Расходы', 'Имеющиеся средства']

    '''for i in unique_list_main:
        
        to_add = [i, i]
        to_add = tuple(to_add)
        analysing_main_tuple.append(to_add)

    analysing_main_tuple = tuple(analysing_main_tuple)

    analysing_main_second_level_tuple  '''

    date_begin = forms.DateField(label ='Дата')
    date_end = forms.DateField(label ='Дата')
    main = forms.CharField(label ='main', required=False)
    firstLEV = forms.CharField(label ='firstLEV', required=False)
    secondLEV = forms.CharField(label ='secondLEV', required=False)

    #analysing_main = forms.TypedChoiceField(label = 'Раздел', choices=first_level_kind_unique_tuple,  coerce = str)
    #analysing_main_first_level = forms.TypedChoiceField(label = 'Основной вид',choices=second_level_kind_unique_tuple, coerce = str)
    #analysing_main_second_level = forms.TypedChoiceField(label = 'Детализация',choices=second_level_kind_unique_tuple, coerce = str)
    #ammount = forms.FloatField(label ='Сумма', help_text="000.00") 
    #comment = forms.CharField(label ='Комментарий', help_text="Any comments?")
   
    def clean_date_begin(self):
        
        data_begin_valid = self.cleaned_data['date_begin']
        
        if str(data_begin_valid) > dateformat.format(timezone.now(), 'Y-m-d'):
            raise ValidationError(_('Invalid date - it is in future'))


        return data_begin_valid


    def clean_date_end(self):
        
        data_end_valid = self.cleaned_data['date_end']
        date_begin = self.cleaned_data['date_begin']
        delta = data_end_valid-date_begin

        if str(data_end_valid) > dateformat.format(timezone.now(), 'Y-m-d'):
            
            raise ValidationError(_('Invalid date - it is in future'))

        if (int(delta.days))<0:

            raise ValidationError(_('Invalid date - time period is negative'))
        
        return data_end_valid

    def clean_main(self):
                
        main_valid = self.cleaned_data['main']
        
        if main_valid=='':

            raise ValidationError(_('Выберите объект анализа'))

        return main_valid  