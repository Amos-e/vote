import uuid
from django.utils.dateparse import parse_date
from django.db.models import Sum, Q

from django.db.models.signals import post_save, pre_delete
from django.contrib.auth import login, logout
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from . import forms
from . import models



def login_view(request):
	if request.method == "POST":

		form = forms.CustomAuthForm(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return redirect("main:dashboard")
	else:
		form = forms.CustomAuthForm()

	return render(request, 'main/login.html', {"form": form})


def logout_view(request):
	if request.method == "POST":
		logout(request)
		return redirect("main:login")


def settings_view(request):

	if request.GET.get('financial_year'):
		year_id = request.GET.get('financial_year')
		years = models.FinancialYear.objects.all()

		for year in years:
			year.active = False
			year.save()
			print(year.active)

		financial_year = models.FinancialYear.objects.get(id=year_id)
		financial_year.active = True
		financial_year.save()

	if request.method == "POST":
		form = forms.FinancialYearForm(request.POST)

		if form.is_valid():
			settings = models.Settings.objects.latest('id')
			form = form.save(commit=False)
			form.settings = settings

			form.save()
			return redirect("main:settings")
	else:
		form = forms.FinancialYearForm()

	financial_years = models.FinancialYear.objects.all()
	current_financial_year = models.FinancialYear.objects.get(active=True)

	context = {
		"form": form,
		"financial_years": financial_years,
		"current_financial_year": current_financial_year,
	}

	return render(request, "main/settings.html", context)


def dashboard_view(request):
	total_members = models.Member.objects.all().count()
	total_transactions = models.Transaction.objects.fn_manager(fn_year()['start'], fn_year()['last']).all().count()
	transactions = models.Transaction.objects.fn_manager(fn_year()['start'], fn_year()['last']).all().order_by('-shares', '-savings', '-welfare')[0:10]
	total_tulinaawe_open = models.Tulinaawe.objects.filter(status=True).count()
	total_tulinaawe_closed = models.Tulinaawe.objects.filter(status=False).count()

	total_loans = models.Loan.objects.fn_manager(fn_year()['start'], fn_year()['last']).count()
	total_expense = models.Expense.objects.fn_manager(fn_year()['start'], fn_year()['last']).all().count()

	context = {
		"total_members": total_members,
		"total_transactions": total_transactions,
		"total_tulinaawe_open": total_tulinaawe_open,
		"total_tulinaawe_closed": total_tulinaawe_closed,
		"total_loans": total_loans,
		"total_expense": total_expense,
		"transactions": transactions,
	}

	return render(request, 'main/dashboard.html', context)


def tulinaawe_view(request):

	all_events = models.Tulinaawe.objects.all()

	if request.method == "POST":
		form = forms.EventForm(request.POST, label_suffix="")
		if form.is_valid():
			form.save()
			return redirect("main:tulinaawe")

	else:
		form = forms.EventForm(label_suffix="")

	paginator = Paginator(all_events, 10)

	if not request.GET.get('page'):
		page = 1
	else:
		page = request.GET.get('page')
		try:
			paginator.page(page)
		except:
			page = 1

	events = paginator.get_page(page)
	page_range = list(paginator.get_elided_page_range(page, on_each_side=2))

	context = {
		"form": form,
		"events": events,
		"page_range": page_range,
	}

	return render(request, "main/tulinaawe.html", context)


def tulinaawe_detail(request, slug):

	event = models.Tulinaawe.objects.get(id=slug)

	if request.GET.get('action') == 'delete' and request.GET.get('modal') == 'tulinaawe':
		event.delete()
		return redirect('main:tulinaawe')

	if request.GET.get('action') == 'delete' and request.GET.get('modal') == 'contributor':
		_id = request.GET.get('id')
		contributor = models.TulinaaweContributor.objects.get(id=_id)
		contributor.delete()
		return redirect(reverse('main:tulinaawe_detail', args=(slug,)))


	if request.method == "POST":
		form = forms.ContributorForm(request.POST, label_suffix="")

		if form.is_valid():
			contributor = form.save(commit=False)
			contributor.event = event
			contributor.save()
			return redirect(reverse("main:tulinaawe_detail", args=(event.id,)))

	else:
		form = forms.ContributorForm(label_suffix="")

	if request.GET.get('status') == "close":
		event.status = False
		event.save()

	elif request.GET.get('status') == "open":
		event.status = True
		event.save()

	total_contributed = 0
	contributors = models.TulinaaweContributor.objects.filter(event=event)
	for contributor in contributors:
		total_contributed += contributor.amount

	context = {
		"event": event,
		"contributors": contributors,
		"total_contributed": total_contributed,
		"form": form,
	}

	return render(request, "main/tulinaawe_detail.html", context)

def members(request):

	if request.method == "POST" and request.POST.get('member-name'):
		name = str(request.POST.get('member-name'))
		members = models.Member.objects.filter(full_names__icontains=name)
		print_ids = ",".join(str(_id) for _id in list(members.values_list('id', flat=True)))

		context = {
			"members": members,
			"print_ids": print_ids,
			"search_term": name,
		}

		return render(request, "main/members.html", context)

	else:
		all_members = models.Member.objects.all()

		paginator = Paginator(all_members, 20)

		if not request.GET.get('page'):
			page = 1
		else:
			page = request.GET.get('page')
			try:
				paginator.page(page)
			except:
				page = 1

		members = paginator.get_page(page)
		page_range = list(paginator.get_elided_page_range(page, on_each_side=2))
		print_ids = ",".join(str(_id) for _id in list(all_members.values_list('id', flat=True)))

		context = {
			"members": members,
			"page_range": page_range,
			"print_ids": print_ids,
		}

		return render(request, 'main/members.html', context)

def fn_year():
	financial_year = models.FinancialYear.objects.get(active=True)
	start_date = financial_year.first_date
	end_date = financial_year.second_date

	return {
		"start": start_date,
		"last": end_date,
	}


def member_transactions(request, slug, slug2):
	member_code = slug + '/' + slug2
	member = models.Member.objects.get(code=member_code)

	if request.method == "POST" and request.POST.get('date_1'):

		comparison = request.POST.get('comparison')
		date_1 = parse_date(request.POST.get('date_1'))
		date_2 = parse_date(request.POST.get('date_2')) if request.POST.get('date_2') else None

		if comparison == 'after':
			transactions = models.Transaction.objects.fn_manager(fn_year()['start'], fn_year()['last']).filter(member=member, date__date__gt=date_1)
			search_term = "After"

		elif comparison == 'before':
			transactions = models.Transaction.objects.fn_manager(fn_year()['start'], fn_year()['last']).filter(member=member, date__date__lt=date_1)
			search_term = "Before"

		elif comparison == 'equal':
			transactions = models.Transaction.objects.fn_manager(fn_year()['start'], fn_year()['last']).filter(member=member, date__date__exact=date_1)
			search_term = "Equal"

		elif comparison == 'month':
			transactions = models.Transaction.objects.fn_manager(fn_year()['start'], fn_year()['last']).filter(member=member, date__year=date_1.year, date__month=date_1.month)
			search_term = ""

		elif comparison == 'between':
			transactions = models.Transaction.objects.fn_manager(fn_year()['start'], fn_year()['last']).filter(member=member, date__range=(date_1, date_2))
			search_term = "Between"

		totals = {
			"shares": 0,
			"savings": 0,
			"withdraw": 0,
			"welfare": 0,
			"fines": 0,
			"other": 0,
			"shares_withdraw": 0,
			"share_value": 0,
			"shares_withdraw_value": 0,
			"net_shares": 0,
			"net_shares_value": 0,
		}

		for transaction in transactions:
			
			if transaction.shares > 0:
				totals['shares'] += transaction.shares
			else:
				totals['shares_withdraw'] -= transaction.shares

			totals["savings"] += transaction.savings
			totals["withdraw"] += transaction.withdraw
			totals["welfare"] += transaction.welfare
			totals["fines"] += transaction.fines
			totals["other"] += transaction.other

		totals["net_shares"] = totals["shares"] - totals["shares_withdraw"]
		totals["share_value"] = totals["shares"] * 5000
		totals['shares_withdraw_value'] = totals["shares_withdraw"] * 5000
		totals["net_shares_value"] = totals["net_shares"] * 5000

		print_ids = ",".join(str(_id) for _id in list(transactions.values_list('id', flat=True)))

		other_present = False
		if totals["other"] > 0:
			other_present = True

		context = {
			"member": member,
			"member_transactions": transactions,
			"totals": totals,
			"print_ids": print_ids,
			"search_term": search_term,
			"date_1": date_1,
			"date_2": date_2,
			"other_present": other_present,
		}

		return render(request, "main/member_transactions.html", context)

	else:

		#This is to correct errors that might arise when post save and post delete do not work
		financial_year = models.FinancialYear.objects.get(active=True)
		all_member_transactions = models.Transaction.objects.filter(member=member)

		if all_member_transactions.exists():
			total_shares = all_member_transactions.aggregate(Sum('shares'))['shares__sum']
			total_savings = all_member_transactions.aggregate(Sum('savings'))['savings__sum']
			total_withdraw = all_member_transactions.aggregate(Sum('withdraw'))['withdraw__sum']
			total_others = all_member_transactions.aggregate(Sum('other'))['other__sum']
			total_fines = all_member_transactions.aggregate(Sum('fines'))['fines__sum']
			total_welfare = all_member_transactions.aggregate(Sum('welfare'))['welfare__sum']

			member.shares = total_shares
			member.savings = total_savings
			member.savings -= total_withdraw
			member.withdraw = total_withdraw
			member.others = total_others
			member.fines = total_fines
			member.welfare = total_welfare

			member.save()

		member_transactions = models.Transaction.objects.fn_manager(fn_year()['start'], fn_year()['last']).filter(member=member).order_by("-date")

		membership_present = False
		membership_value = 0

		if request.GET.get('membership') == "True":
			membership_present = True
			member_transactions = models.Transaction.objects.fn_manager(fn_year()['start'], fn_year()['last']).filter(member=member, notes__icontains="member")
			membership_value = member_transactions.aggregate(Sum('other'))['other__sum']

		chairs_present = False
		chairs_value = 0
		
		if request.GET.get('chairs') == "True":
			chairs_present = True
			member_transactions = models.Transaction.objects.fn_manager(fn_year()['start'], fn_year()['last']).filter(member=member, notes__icontains="chair")
			chairs_value = member_transactions.aggregate(Sum('other'))['other__sum']

		loans_present = False
		loans_value = 0

		if request.GET.get('loans') == "True":
			loans_present = True
			member_transactions = models.Transaction.objects.fn_manager(fn_year()['start'], fn_year()['last']).filter(member=member, notes__icontains='loan').exclude(notes__icontains="loan form").exclude(notes__icontains="loans form").exclude(notes__icontains="loan forms")
			loans_value = member_transactions.aggregate(Sum('other'))['other__sum']


		loan_form_present = False
		loan_form_value = 0

		if request.GET.get('loan_form') == "True":
			loan_form_present = True
			member_transactions = models.Transaction.objects.fn_manager(fn_year()['start'], fn_year()['last']).filter(member=member, notes__icontains='loan form')
			loan_form_value = member_transactions.aggregate(Sum('other'))['other__sum']



		uniforms_present = False
		uniforms_value = 0

		if request.GET.get('uniforms') == "True":
			uniforms_present = True
			member_transactions = models.Transaction.objects.fn_manager(fn_year()['start'], fn_year()['last']).filter(member=member, notes__icontains="uniform")
			uniforms_value = member_transactions.aggregate(Sum('other'))['other__sum']


		renewal_present = False
		renewal_value = 0

		if request.GET.get('renewal') == "True":
			renewal_present = True
			member_transactions = models.Transaction.objects.fn_manager(fn_year()['start'], fn_year()['last']).filter(member=member, notes__icontains="renewal")
			renewal_value = member_transactions.aggregate(Sum('other'))['other__sum']


		plates_present = False
		plates_value = 0

		if request.GET.get('plates') == "True":
			plates_present = True
			member_transactions = models.Transaction.objects.fn_manager(fn_year()['start'], fn_year()['last']).filter(member=member, notes__icontains="plate")
			plates_value = member_transactions.aggregate(Sum('other'))['other__sum']


		closing_balance_present = False
		closing_balance_value = 0

		if request.GET.get('closing_balance') == "True":
			closing_balance_present = True
			member_transactions = models.Transaction.objects.fn_manager(fn_year()['start'], fn_year()['last']).filter(member=member, notes__icontains="closing balance")
			closing_balance_value = member_transactions.aggregate(Sum('other'))['other__sum']

		shares = 0
		shares_withdraw = 0
		shares_value = 0
		shares_withdraw_value = 0
		net_shares = 0
		net_shares_value = 0

		savings = 0
		withdraw = 0
		welfare = 0
		fines = 0
		other = 0

		for transaction in member_transactions:
			if transaction.shares > 0:
				shares += transaction.shares
			else:
				shares_withdraw -= transaction.shares

			savings += transaction.savings
			withdraw += transaction.withdraw
			welfare += transaction.welfare
			fines += transaction.fines
			other += transaction.other
			
		savings = savings - withdraw

		net_shares = shares - shares_withdraw

		net_shares_value = net_shares * 5000
		shares_value = shares * 5000
		shares_withdraw_value = shares_withdraw * 5000
		
		paginator = Paginator(member_transactions, 100)

		if not request.GET.get('page'):
			page = 1
		else:
			page = request.GET.get('page')
			try:
				paginator.page(page)
			except:
				page = 1

		transactions = paginator.get_page(page)
		page_range = list(paginator.get_elided_page_range(page, on_each_side=2))
		print_ids = ",".join(str(_id) for _id in list(member_transactions.values_list('id', flat=True)))

		other_present = False
		for transaction in transactions:
			if transaction.other > 0:
				other_present = True
				break

		context = {
			"member": member,

			"shares": shares,
			"shares_withdraw": shares_withdraw,
			"shares_value": shares_value,
			"shares_withdraw_value": shares_withdraw_value,
			"net_shares": net_shares,
			"net_shares_value": net_shares_value,

			"savings": savings,
			"withdraw": withdraw,
			"welfare": welfare,
			"other": other,
			"fines": fines, 

			"member_transactions": transactions,
			"page_range": page_range,
			"print_ids": print_ids,

			"other_present": other_present,
			"membership_present": membership_present,
			"chairs_present": chairs_present,
			"loans_present": loans_present,
			"loan_form_present": loan_form_present,
			"uniforms_present": uniforms_present,
			"renewal_present": renewal_present,
			"plates_present": plates_present,
			"closing_balance_present": closing_balance_present,

			"membership_value": membership_value,
			"chairs_value": chairs_value,
			"loans_value": loans_value,
			"uniforms_value": uniforms_value,
			"renewal_value": renewal_value,
			"loan_form_value": loan_form_value,
			"plates_value": plates_value,
			"closing_balance_value": closing_balance_value,
		}

		return render(request, "main/member_transactions.html", context)


def member_info(request):

	if request.GET.get('action') == 'detail':
		member = models.Member.objects.get(id=request.GET.get('id'))
		name = member.full_name
		image = member.image.url
		shares = member.shares
		savings = member.savings

		context = {
			"name": name,
			"image": image,
			"shares": shares,
			"savings": savings,
		}

		return JsonResponse(context, safe=False)


def transaction_view(request, slug):

	if request.GET.get('action') == 'delete':
		transaction = models.Transaction.objects.get(id=slug)
		transaction.delete()

		referer = request.GET.get('referer')

		if referer == 'member-transactions':
			member_code = request.GET.get('member-code').split('/')
			code_1 = member_code[0]
			code_2 = member_code[1]
			return redirect(reverse("main:member_transactions", args=(code_1, code_2,)))

		else:
			return redirect("main:all_transactions")


def transaction_detail(request, slug):
	
	transaction = models.Transaction.objects.get(id=int(slug))
	member = transaction.member
	edit_date = transaction.date
	form = forms.TransactionDetail(instance=transaction, label_suffix="")

	context = {
		"form": form,
		"edit": True,
		"edit_date": edit_date,
		"member": member,
		"transaction_id": transaction.id,
	}

	return render(request, 'main/form_view/transaction_detail.html', context)


def all_transactions(request):

	financial_year = models.FinancialYear.objects.get(active=True)

	totals = {
		"shares": 0,
		"savings": 0,
		"withdraw": 0,
		"welfare": 0,
		"fines": 0,
		"other": 0,
		"share_value": 0,
		"share_withdraw": 0,
		"total": 0,
	}

	if request.method == "POST" and request.POST.get('date_1') and request.POST.get('comparison'):

		comparison = request.POST.get('comparison')
		date_1 = parse_date(request.POST.get('date_1'))
		date_2 = parse_date(request.POST.get('date_2')) if request.POST.get('date_2') else None

		if comparison == 'after':
			transactions = models.Transaction.objects.fn_manager(fn_year()['start'], fn_year()['last']).filter(date__date__gt=date_1)
			search_term = "after"

		elif comparison == 'before':
			transactions = models.Transaction.objects.fn_manager(fn_year()['start'], fn_year()['last']).filter(date__date__lt=date_1)
			search_term = "before"

		elif comparison == 'equal':
			transactions = models.Transaction.objects.fn_manager(fn_year()['start'], fn_year()['last']).filter(date__date__exact=date_1)
			search_term = "equal"

		elif comparison == 'month':
			transactions = models.Transaction.objects.fn_manager(fn_year()['start'], fn_year()['last']).filter(date__year=date_1.year, date__month=date_1.month)
			search_term = "month"

		elif comparison == 'between':
			transactions = models.Transaction.objects.fn_manager(fn_year()['start'], fn_year()['last']).filter(date__range=(date_1, date_2))
			search_term = "between"

		for transaction in transactions:
			if transaction.shares < 0:
				totals["share_withdraw"] -= transaction.shares
			else:	
				totals["shares"] += transaction.shares
			totals["savings"] += transaction.savings
			totals["withdraw"] += transaction.withdraw
			totals["welfare"] += transaction.welfare
			totals["fines"] += transaction.fines
			totals["other"] += transaction.other

		# totals["shares"] = transactions.aggregate(Sum('shares'))['shares__sum']
		# totals["savings"] = transactions.aggregate(Sum('savings'))['savings__sum']
		# totals["withdraw"] = transactions.aggregate(Sum('withdraw'))['withdraw__sum']
		# totals["welfare"] = transactions.aggregate(Sum('welfare'))['welfare__sum']
		# totals["fines"] = transactions.aggregate(Sum('fines'))['fines__sum']
		# totals["other"] = transactions.aggregate(Sum('other'))['other__sum']


		totals["share_value"] = totals["shares"] * 5000

		for key, value in totals.items():
			if key == "shares" or key == "total" or key == "share_withdraw" or key == "share_withdraw_value" or key == "withdraw":
				continue
			else:
				totals["total"] += value

		totals["share_withdraw_value"] = totals["share_withdraw"] * 5000
		totals['net_total'] = totals['total']-totals['withdraw']-(totals['share_withdraw']*5000)

		print_ids = ",".join(str(_id) for _id in list(transactions.values_list('id', flat=True)))

		other_present = False
		if totals["other"] != 0:
			other_present = True

		context = {
			"transactions": transactions,
			"totals": totals,
			"print_ids": print_ids,
			"search_term": search_term,
			"date_1": date_1,
			"date_2": date_2,
			"other_present": other_present,
		}

		return render(request, "main/all_transactions.html", context)

	else:

		year = request.GET.get('year')
		month = request.GET.get('month')
		day = request.GET.get('day')

		if request.GET.get('settings') == 'results_order':
			settings = models.Settings.objects.get(id=1)
			
			if request.GET.get('value') == 'show last added':
				settings.results_order = 'show latest date'
			else:
				settings.results_order = 'show last added'

			settings.save()

		settings = models.Settings.objects.get(id=1)

		latest_transaction = models.Transaction.objects.latest("id")
		latest_date =  models.Transaction.objects.latest('date')

		if settings.results_order == 'show last added':
			all_transactions = models.Transaction.objects.fn_manager(fn_year()['start'], fn_year()['last']).filter(date=latest_transaction.date)
			date_1 = latest_transaction.date
		else:
			all_transactions = models.Transaction.objects.fn_manager(fn_year()['start'], fn_year()['last']).filter(date=latest_date.date)
			date_1 = latest_date.date

		# all_transactions = models.Transaction.objects.filter(date=latest_transaction.date)

		paginator = Paginator(all_transactions, 50)

		if not request.GET.get('page'):
			page = 1
		else:
			page = request.GET.get('page')
			try:
				paginator.page(page)
			except:
				page = 1

		transactions = paginator.get_page(page)
		page_range = list(paginator.get_elided_page_range(page, on_each_side=2))

		for transaction in all_transactions:
			if transaction.shares < 0:
				totals['share_withdraw'] -= transaction.shares
			else:
				totals["shares"] += transaction.shares
			totals["savings"] += transaction.savings
			totals["withdraw"] += transaction.withdraw
			totals["welfare"] += transaction.welfare
			totals["fines"] += transaction.fines
			totals["other"] += transaction.other

		# totals["shares"] = all_transactions.aggregate(Sum('shares'))['shares__sum']
		# totals["savings"] = all_transactions.aggregate(Sum('savings'))['savings__sum']
		# totals["withdraw"] = all_transactions.aggregate(Sum('withdraw'))['withdraw__sum']
		# totals["welfare"] = all_transactions.aggregate(Sum('welfare'))['welfare__sum']
		# totals["fines"] = all_transactions.aggregate(Sum('fines'))['fines__sum']
		# totals["other"] = all_transactions.aggregate(Sum('other'))['other__sum']

		totals["share_value"] = totals["shares"] * 5000

		for key, value in totals.items():
			if key == "shares" or key == "total" or key == "share_withdraw" or key == "share_withdraw_value" or key == "withdraw":
				continue
			else:
				totals["total"] += value

		totals["share_withdraw_value"] = totals["share_withdraw"] * 5000
		totals["net_total"] = totals['total']-totals['withdraw']-(totals['share_withdraw']*5000)

		print_ids = ",".join(str(_id) for _id in list(all_transactions.values_list('id', flat=True)))
		search_term = "The Date"
		# date_1 = latest_transaction.date

		other_present = False
		for transaction in transactions:
			if transaction.other != 0:
				other_present = True
				break

		context = {
			"transactions": transactions,
			"page_range": page_range,
			"totals": totals,
			"print_ids": print_ids,
			"other_present": other_present,
			"search_term": search_term,
			"date_1": date_1,
			"settings": settings,
		}

		return render(request, "main/all_transactions.html", context)


def new_member(request):
	if request.method == "POST":
		member_form = forms.MemberCreate(request.POST, request.FILES, label_suffix="")

		#Nominees for Benefits

		if member_form.is_valid():
			member_form.save()
			return redirect("main:new_member")
	else:
		member_form = forms.MemberCreate(label_suffix="")

	date_fields = []

	for field in member_form.fields:
		if 'date' in field:
			date_fields.append(field)

	context = {
		"form": member_form,
		"date_fields": date_fields,
	}

	return render(request, 'main/new_member.html', context)


def update_member(request):

	if request.method == "POST":
		member_code = request.POST.get('code')
		member = models.Member.objects.get(code=member_code)
		member_form = forms.MemberCreate(request.POST, instance=member, label_suffix="")

		if member_form.is_valid():
			member_form.save()
			return redirect("main:members")

	else:
		member_code = request.GET.get('member-code')
		member = models.Member.objects.get(code=member_code)
		member_form = forms.MemberCreate(instance=member, label_suffix="")

	return render(request, "main/update_member.html", {"form": member_form})


def member_new_transaction(request, slug, slug2):
	member_code = slug + '/' + slug2
	member = models.Member.objects.get(code=member_code)
	member_detail_count = models.Transaction.objects.all().count()
	latest_transaction = 0

	if member_detail_count > 0:
		latest_transaction = models.Transaction.objects.latest("id")

	if request.method == "POST":
		form = forms.Transaction(request.POST, label_suffix="")

		if form.is_valid():
			detail = form.save(commit=False)
			detail.member = member
			detail.save()

			return redirect("main:members")
	else:
		form = forms.Transaction(label_suffix="")

	latest_date = models.Transaction.objects.latest('id').date.date

	context = {
		"form": form,
		"member": member,
		"latest_date": latest_date,
	}

	return render(request, 'main/member_new_transaction.html', context)


def new_transaction(request):

	# POST FUNCTION

	if request.method == "POST":
		form = forms.TransactionForm(request.POST)
		edit = request.POST.get('edit')

		if edit == "True":
			transaction_id = int(request.POST.get('transaction-id'))
			member = models.Member.objects.get(id=request.POST.get('member'))
			transaction = models.Transaction.objects.get(id=transaction_id)

			if transaction.member == member:
				transaction.delete()

		if form.is_valid():
			form.save()
			return redirect("main:new_transaction")
	else:
		form = forms.TransactionForm(label_suffix="", initial={"notes": ""})

	latest_date = models.Transaction.objects.latest('id').date.date
	latest_transaction = models.Transaction.objects.latest('id')

	context = {
		"form": form,
		"latest_date": latest_date,
		"latest_transaction": latest_transaction,
	}

	# GET FUNCTIONS

	if request.GET.get('action') == 'detail':
		member = models.Member.objects.get(id=request.GET.get('id'))
		data = {
			"code": member.code,
			"full_name": member.full_name,
			"image": member.image.url
		}
		return JsonResponse(data, safe=False)


	if request.GET.get('action') == 'member-transaction':
		member = models.Member.objects.get(code=request.GET.get('code'))
		form = forms.TransactionForm(label_suffix="", initial={"member": member})

		context.update({
			"form": form,
			"member_transaction": True,
			"member": member,
		})


	if request.GET.get('action') == 'edit':
		transaction = models.Transaction.objects.get(id=request.GET.get('id'))
		member = transaction.member
		edit_date = transaction.date
		form = forms.TransactionForm(instance=transaction, label_suffix="")

		context.update({
			"form": form,
			"edit": True,
			"edit_date": edit_date,
			"member": member,
			"transaction_id": transaction.id,
		})

	return render(request, "main/new_transaction.html", context)


def welfare_view(request):

	members = models.Member.objects.exclude(code="KYDI/000")
	transactions = models.Transaction.objects.fn_manager(fn_year()['start'], fn_year()['last']).all()

	total_members = members.count()
	total_welfare = 104000 * total_members
	total_welfare_paid = transactions.aggregate(Sum('welfare'))["welfare__sum"]
	total_welfare_balance = total_welfare - total_welfare_paid

	welfares = {}

	for member in members:
		welfare = transactions.filter(member=member).aggregate(Sum('welfare'))["welfare__sum"]
		try:
			welfare_balance = 104000 - welfare
		except TypeError:
			welfare_balance = 0 

		welfares[member] = {
			"welfare": welfare,
			"balance": welfare_balance
		}

	context = {
		"total_members": total_members,
		"total_welfare": total_welfare,
		"total_welfare_paid": total_welfare_paid,
		"total_welfare_balance": total_welfare_balance,
		"welfares": welfares
	}

	return render(request, "main/welfare.html", context)


def shares_view(request):
	members = models.Member.objects.exclude(code="KYDI/000")
	transactions = models.Transaction.objects.fn_manager(fn_year()['start'], fn_year()['last']).all()

	total_members = members.count()
	total_shares = transactions.aggregate(Sum('shares'))['shares__sum']
	


def savings_withdraw_view(request):

	members = models.Member.objects.exclude(code="KYDI/000")
	transactions = models.Transaction.objects.fn_manager(fn_year()['start'], fn_year()['last']).all()

	total_members = members.count()
	total_savings = transactions.aggregate(Sum('savings'))['savings__sum']
	total_withdraw = transactions.aggregate(Sum('withdraw'))['withdraw__sum']
	total_net_savings = total_savings - total_withdraw

	savings_withdraws = {}

	for member in members:

		savings = transactions.filter(member=member).aggregate(Sum('savings'))['savings__sum']
		withdraw = transactions.filter(member=member).aggregate(Sum('withdraw'))['withdraw__sum']

		try:
			net_savings = savings - withdraw
		except TypeError:
			net_savings = 0

		savings_withdraws[member] = {
			"savings": savings,
			"withdraw": withdraw,
			"net_savings": net_savings,
		}

	context = {
		"total_members": total_members,
		"total_savings": total_savings,
		"total_withdraw": total_withdraw,
		"total_net_savings": total_net_savings,
		"savings_withdraws": savings_withdraws
	}

	return render(request, "main/savings_withdraw.html", context)


def loans_view(request):

	all_loans = models.Loan.objects.fn_manager(fn_year()['start'], fn_year()['last']).all().order_by('member')
	paid_or_unpaid = False

	if request.GET.get('action') == 'paid-loans':
		all_loans = models.Loan.objects.fn_manager(fn_year()['start'], fn_year()['last']).filter(interest__gt=0)
		paid_or_unpaid = True

	if request.GET.get('action') == 'unpaid-loans':
		all_loans = models.Loan.objects.fn_manager(fn_year()['start'], fn_year()['last']).filter(interest=0)
		paid_or_unpaid = True

	loans_count = all_loans.count()

	total_amount = models.Loan.objects.fn_manager(fn_year()['start'], fn_year()['last']).all().aggregate(Sum('amount'))['amount__sum']

	total_amount_paid = models.Loan.objects.fn_manager(fn_year()['start'], fn_year()['last']).all().aggregate(Sum('amount_paid'))['amount_paid__sum']
	
	total_interest = models.Loan.objects.fn_manager(fn_year()['start'], fn_year()['last']).all().aggregate(Sum('interest'))['interest__sum']

	if request.method == "POST" and request.POST.get('member-name'):
		member_name = request.POST.get('member-name')
		all_loans = models.Loan.objects.fn_manager(fn_year()['start'], fn_year()['last']).filter(member_name__icontains=member_name)

	paginator = Paginator(all_loans, 100)

	if request.method == "POST":
		form = forms.LoanForm(request.POST, label_suffix="")

		if form.is_valid():
			form.save()
			return redirect("main:loans")

	else:
		form = forms.LoanForm(label_suffix="")

	loans = models.Loan.objects.fn_manager(fn_year()['start'], fn_year()['last']).all()

	if not request.GET.get('page'):
		page = 1
	else:
		page = request.GET.get('page')
		try:
			paginator.page(page)
		except:
			page = 1

	loans = paginator.get_page(page)
	page_range = list(paginator.get_elided_page_range(page, on_each_side=2))

	context = {
		"all_loans": all_loans,
		"paid_or_unpaid": paid_or_unpaid,
		"form": form,
		"loans": loans,
		"page_range": page_range,
		"loans_count": loans_count,
		"total_amount": total_amount,
		"total_amount_paid": total_amount_paid,
		"total_interest": total_interest,
	}

	return render(request, "main/loans.html", context)


def loan_detail(request, slug):

	loan = models.Loan.objects.get(id=slug)

	if request.GET.get('action') == 'delete' and request.GET.get('modal') == 'loan':
		loan.delete()
		return redirect("main:loans")

	if request.GET.get('action') == 'delete' and request.GET.get('modal') == 'loan-payment':
		loan_payment_id = request.GET.get('id')
		loan_payment = models.LoanPayment.objects.get(id=loan_payment_id)
		loan_payment.delete()
		return redirect(reverse('main:loan_detail', args=(slug,)))

	if request.method == "POST":
		form = forms.LoanPaymentForm(request.POST, label_suffix="")
		if form.is_valid():
			loan_payment = form.save(commit=False)
			loan_payment.loan = loan
			loan_payment.save()
			return redirect(reverse("main:loan_detail", args=(loan.id,)))
	else:
		form = forms.LoanPaymentForm(label_suffix="")

	loan_payments = models.LoanPayment.objects.filter(loan=loan)

	context = {
		"form": form,
		"loan": loan,
		"loan_payments": loan_payments,
	}

	return render(request, "main/loan_detail.html", context)


def reports_api(request):

	months = [
		'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'
	]

	year = request.GET.get('year')
	month = request.GET.get('month')
	day = request.GET.get('day')
	

	if not year:
		year = models.Transaction.objects.fn_manager(fn_year()['start'], fn_year()['last']).latest('date').date.year

	transactions = models.Transaction.objects.fn_manager(fn_year()['start'], fn_year()['last']).filter(date__year=year)

	#Handles available months i.e months with transactions are the only ones that are displayed.
	search_months_query = transactions.dates('date', 'month')
	search_months = {}

	for search_month in search_months_query:
		search_months[search_month.month] = months[search_month.month - 1]

	#Then fetch transactions of a specific month if month present in request
	if month:
		transactions = transactions.filter(date__month=month)

	#Handles available days i.e days with transactions
	if month:
		search_days_query = transactions.dates('date', 'day')
	else:
		search_days_query = transactions.filter(date__month=search_months_query[0].month).dates('date', 'day')
	search_days = []

	for search_day in search_days_query:
		search_days.append(search_day.day)

	#Fetch transactions of a specific day if day present in request
	if day:
		transactions = transactions.filter(date__day=day)	


	total_shares = 0
	total_shares_withdraw = 0

	for transaction in transactions:
		if transaction.shares < 0:
			total_shares_withdraw = total_shares_withdraw - transaction.shares
		else:
			total_shares = total_shares + transaction.shares

	total_welfare = transactions.aggregate(Sum('welfare'))['welfare__sum']
	total_savings = transactions.aggregate(Sum('savings'))['savings__sum']
	total_withdraw = transactions.aggregate(Sum('withdraw'))['withdraw__sum']
	total_fines = transactions.aggregate(Sum('fines'))['fines__sum']
	total_other = transactions.aggregate(Sum('other'))['other__sum']

	net_shares = total_shares - total_shares_withdraw

	data = {
		'year': year,
		'totals': {},
		'search_months': search_months,
		'search_days': search_days,
		'total': {
			'shares': total_shares,
			'shares_withdraw': total_shares_withdraw,
			'net_shares': net_shares,
			'welfare': total_welfare,
			'savings': total_savings,
			'withdraw': total_withdraw,
			'fines': total_fines,
			'other': total_other, 
		}
	}

	month_counter = 1

	if not month:

		data['chart_type'] = 'year'

		for month in months:

			month_transactions = transactions.filter(date__month=month_counter)

			data['totals'][month] = {
				"shares": month_transactions.aggregate(Sum("shares"))['shares__sum'],
				"welfare": month_transactions.aggregate(Sum("welfare"))['welfare__sum'],
				"savings": month_transactions.aggregate(Sum("savings"))['savings__sum'],
				"withdraw": month_transactions.aggregate(Sum("withdraw"))['withdraw__sum'],
				"fines": month_transactions.aggregate(Sum("fines"))['fines__sum'],
				"other": month_transactions.aggregate(Sum("other"))['other__sum'],
				"total_transactions": month_transactions.count()
			}

			month_counter += 1

	elif month and not day:

		data['chart_type'] = 'month'

		days_query = transactions.dates('date', 'day')

		for day in days_query:
			day_transactions = transactions.filter(date__day=day.day)

			data['totals'][day.strftime('%x')] = {
				'shares': day_transactions.aggregate(Sum('shares'))['shares__sum'],
				'welfare': day_transactions.aggregate(Sum('welfare'))['welfare__sum'],
				'savings': day_transactions.aggregate(Sum('savings'))['savings__sum'],
				'withdraw': day_transactions.aggregate(Sum('withdraw'))['withdraw__sum'],
				'fines': day_transactions.aggregate(Sum('fines'))['fines__sum'],
				'other': day_transactions.aggregate(Sum('other'))['other__sum'],
				'total_transactions': day_transactions.count(),
			}
		
	elif month and day:

		data['chart_type'] = 'day'

		for transaction in transactions:

			transaction_related = transactions.filter(member=transaction.member)

			data['totals'][transaction.member.code] = {
				'shares': transaction_related.aggregate(Sum('shares'))['shares__sum'],
				'welfare': transaction_related.aggregate(Sum('welfare'))['welfare__sum'],
				'savings': transaction_related.aggregate(Sum('savings'))['savings__sum'],
				'withdraw': transaction_related.aggregate(Sum('withdraw'))['withdraw__sum'],
				'fines': transaction_related.aggregate(Sum('fines'))['fines__sum'],
				'other': transaction_related.aggregate(Sum('other'))['other__sum'],
				'total_transactions': 1,
			}

	return JsonResponse(data)


def member_report_api(request):

	months = [
		'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'
	]

	year = request.GET.get('year')
	month = request.GET.get('month')
	day = request.GET.get('day')
	member_code = request.GET.get('code')

	member = models.Member.objects.get(code=member_code)

	if not year:
		year = models.Transaction.objects.filter(member=member).latest('date').date.year

	transactions = models.Transaction.objects.filter(member=member, date__year=year)


	search_months_query = transactions.dates('date', 'month')
	search_months = {}

	for search_month in search_months_query:
		search_months[search_month.month] = months[search_month.month - 1]


	if month:
		transactions = transactions.filter(date__month=month)

	total_transactions = transactions.count()
	total_shares = transactions.aggregate(Sum('shares'))['shares__sum']
	total_welfare = transactions.aggregate(Sum('welfare'))['welfare__sum']
	total_savings = transactions.aggregate(Sum('savings'))['savings__sum']
	total_withdraw = transactions.aggregate(Sum('withdraw'))['withdraw__sum']
	total_fines = transactions.aggregate(Sum('fines'))['fines__sum']
	total_other = transactions.aggregate(Sum('other'))['other__sum']

	data = {
		'year': year,
		'totals': {},
		'search_months': search_months,
		'total': {
			'shares': total_shares,
			'welfare': total_welfare,
			'savings': total_savings,
			'withdraw': total_withdraw,
			'fines': total_fines,
			'other': total_other, 
		}
	}

	month_counter = 1

	if not month:

		data['chart_type'] = 'year'

		for month in months:

			month_transactions = transactions.filter(date__month=month_counter)

			data['totals'][month] = {
				"shares": month_transactions.aggregate(Sum("shares"))['shares__sum'],
				"welfare": month_transactions.aggregate(Sum("welfare"))['welfare__sum'],
				"savings": month_transactions.aggregate(Sum("savings"))['savings__sum'],
				"withdraw": month_transactions.aggregate(Sum("withdraw"))['withdraw__sum'],
				"fines": month_transactions.aggregate(Sum("fines"))['fines__sum'],
				"other": month_transactions.aggregate(Sum("other"))['other__sum'],
				"total_transactions": month_transactions.count()
			}

			month_counter += 1

	elif month and not day:

		data['chart_type'] = 'month'

		days_query = transactions.dates('date', 'day')

		for day in days_query:
			day_transactions = transactions.filter(date__day=day.day)

			data['totals'][day.strftime('%x')] = {
				'shares': day_transactions.aggregate(Sum('shares'))['shares__sum'],
				'welfare': day_transactions.aggregate(Sum('welfare'))['welfare__sum'],
				'savings': day_transactions.aggregate(Sum('savings'))['savings__sum'],
				'withdraw': day_transactions.aggregate(Sum('withdraw'))['withdraw__sum'],
				'fines': day_transactions.aggregate(Sum('fines'))['fines__sum'],
				'other': day_transactions.aggregate(Sum('other'))['other__sum'],
				'total_transactions': day_transactions.count(),
			}

	return JsonResponse(data)


def reports_view(request):

	months = [
		'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'
	]

	totals = {
		"shares": 0,
		"savings": 0,
		"withdraw": 0,
		"welfare": 0,
		"fines": 0,
		"other": 0,
		"share_value": 0,
	}

	years = models.Transaction.objects.dates('date', 'year').reverse()
	latest_year = models.Transaction.objects.latest('date').date.year

	all_transactions_search = models.Transaction.objects.filter(date__year=latest_year)

	all_transactions = models.Transaction.objects.fn_manager(fn_year()['start'], fn_year()['last']).filter(date__year=latest_year)

	search_months_query = all_transactions_search.dates('date', 'month')
	search_months = {}

	for month in search_months_query:
		search_months[month.month] = months[month.month - 1]

	search_days_query = all_transactions_search.filter(date__month=search_months_query[0].month).dates('date', 'day')
	search_days = []

	for day in search_days_query:
		search_days.append(day.day)

	for transaction in all_transactions:
		totals["shares"] += transaction.shares
		totals["savings"] += transaction.savings
		totals["withdraw"] += transaction.withdraw
		totals["welfare"] += transaction.welfare
		totals["fines"] += transaction.fines
		totals["other"] += transaction.other

	totals["share_value"] = totals["shares"] * 5000

	context = {
		"totals": totals,
		"years": years,
		"search_months": search_months,
		"search_days": search_days,
	}

	return render(request, "main/reports.html", context)


def member_report(request):

	months = [
		'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'
	]

	totals = {
		"shares": 0,
		"savings": 0,
		"withdraw": 0,
		"welfare": 0,
		"fines": 0,
		"other": 0,
		"share_value": 0,
	}

	member_code = request.GET.get('code')
	member = models.Member.objects.get(code=member_code)

	years = models.Transaction.objects.dates('date', 'year').reverse()
	latest_year = models.Transaction.objects.filter(member=member).latest('date').date.year

	all_transactions = models.Transaction.objects.filter(member=member, date__year=latest_year)

	search_months_query = all_transactions.dates('date', 'month')
	search_months = {}

	for month in search_months_query:
		search_months[month.month] = months[month.month - 1]

	for transaction in all_transactions:
		totals["shares"] += transaction.shares
		totals["savings"] += transaction.savings
		totals["withdraw"] += transaction.withdraw
		totals["welfare"] += transaction.welfare
		totals["fines"] += transaction.fines
		totals["other"] += transaction.other

	totals["share_value"] = totals["shares"] * 5000

	context = {
		"member": member,
		"totals": totals,
		"years": years,
		"search_months": search_months,
	}

	return render(request, 'main/member_report.html', context)


def loan_application_view(request):
	if request.method == "POST":
		loan_form = forms.LoanForm(request.POST, request.FILES, label_suffix="")

		if loan_form.is_valid():
			loan_form.save()
			return redirect("main:loans")
	else:
		loan_form = forms.LoanForm(label_suffix="")

	date_fields = []

	for field in loan_form.fields:
		if 'date' in field:
			date_fields.append(field)

	context = {
		"form": loan_form,
		"date_fields": date_fields,
	}

	return render(request, 'main/loan_application.html', context)


def loan_application_detail_view(request, slug):

	loan = models.Loan.objects.get(id=slug)
	form = forms.LoanForm(instance=loan)

	context = {
		"loan": loan,
		"form": form,
	}

	return render(request, "main/loan_application_detail.html", context)


def expenses_view(request):
	if request.method == "POST":
		form = forms.ExpensesForm(request.POST, label_suffix="")
		if form.is_valid():
			expense = form.save()
			return redirect(reverse('main:expenses_detail', args=(expense.id,)))
	else:
		form = forms.ExpensesForm(label_suffix="")

	receipts = models.Expense.objects.fn_manager(fn_year()['start'], fn_year()['last']).all().order_by('-receipt_no')
	total_amount = models.Expense.objects.fn_manager(fn_year()['start'], fn_year()['last']).all().aggregate(Sum('total_amount'))['total_amount__sum']

	context = {
		"form": form,
		"receipts": receipts,
		"total_amount": total_amount,
	}
	return render(request, "main/expenses.html", context)



def expenses_detail(request, slug):
	expense = models.Expense.objects.get(id=slug)

	if request.GET.get('action') == 'delete' and request.GET.get('modal') == 'expense':
		expense.delete()
		return redirect('main:expenses')

	if request.GET.get('action') == 'delete' and request.GET.get('modal') == 'expense-item':
		_id = request.GET.get('id')
		expense_item = models.ExpenseItem.objects.get(id=_id)
		expense_item.delete()
		return redirect(reverse('main:expenses_detail', args=(slug,)))


	if request.method == "POST":
		form = forms.ExpenseItem(request.POST, label_suffix="")
		if form.is_valid():
			expense_item = form.save(commit=False)
			expense_item.expense = expense
			expense_item.save()
			return redirect(reverse("main:expenses_detail", args=(slug,)))
	else:
		form = forms.ExpenseItem(label_suffix="")


	expense_items = models.ExpenseItem.objects.filter(expense=expense)

	context = {
		"form": form,
		"expense": expense,
		"expense_items": expense_items,
	}

	return render(request, "main/expense_detail.html", context)


def notes_view(request):

	if request.method == "POST":
		form = forms.NotesForm(request.POST, label_suffix="")

		if form.is_valid():
			form.save()
			return redirect('main:notes')

	else:
		form = forms.NotesForm(label_suffix="")

	if request.GET.get('action') == "delete":
		note_id = request.GET.get('id')
		note = models.Note.objects.get(id=note_id)
		note.delete()

	notes = models.Note.objects.all()

	context = {
		"form": form,
		"notes": notes,
	}

	return render(request, "main/notes.html", context)


def convert_savings(request, slug, slug2):
	member_code = slug + '/' + slug2
	member = models.Member.objects.get(code=member_code)

	if request.method == "POST":
		form = forms.Transaction(request.POST, label_suffix="")

		if form.is_valid():
			transaction = form.save(commit=False)
			transaction.member = member
			transaction.save()
			return redirect("main:members")

	else:
		form = forms.Transaction(label_suffix="")

	return render(request, "main/convert_savings.html", {"form": form, "member": member})


def pay_using_shares(request, slug, slug2):
	member_code = slug + '/' + slug2
	member = models.Member.objects.get(code=member_code)

	if request.method == "POST":
		form = forms.Transaction(request.POST)

		if form.is_valid():
			transaction = form.save(commit=False)
			transaction.member = member
			transaction.save()
			return redirect("main:members")

	else:
		form = forms.Transaction(label_suffix="")

	return render(request, "main/pay_using_shares.html", {"form": form, "member": member})


def print_view(request):
	ids = request.GET.get('ids')
	ids = ids.split(',')

	if request.GET.get("context") == "members":
		members = models.Member.objects.in_bulk(ids)
		context = {"members": members}

	if request.GET.get("context") == "member-transactions":
		member = models.Transaction.objects.get(id=ids[0]).member
		member_transactions = models.Transaction.objects.in_bulk(ids)
		context = {"member": member, "member_transactions":  member_transactions}

	if request.GET.get("context") == "transactions-all":
		transactions = models.Transaction.objects.in_bulk(ids)
		context = {"transactions": transactions}

	return render(request, "main/print.html", context)


def transaction_post_save(sender, instance, created, **kwargs):

	if created:

		member = instance.member
		member.shares += instance.shares
		member.savings += instance.savings
		member.savings -= instance.withdraw
		member.withdraw += instance.withdraw
		member.welfare += instance.welfare
		member.fines += instance.fines
		member.other += instance.other
		member.save()

		transaction_type = models.TransactionType.objects.create(transaction=instance)

		if instance.shares > 0 or instance.savings > 0 or instance.welfare > 0:
			transaction_type.general = True

		if instance.withdraw > 0:
			transaction_type.withdraw = True

		if instance.fines > 0:
			transaction_type.fined = True

		if instance.savings < 0:
			transaction_type.savings_to_shares = True

		if instance.fines < 0:
			transaction_type.paid_fines = True

		if instance.shares < 0:
			transaction_type.share_pay = True

		transaction_type.save()

	else:
		pass


def transaction_pre_delete(sender, instance, **kwargs):
	member = instance.member
	member.shares -= instance.shares
	member.savings -= instance.savings
	member.savings += instance.withdraw
	member.withdraw -= instance.withdraw
	member.welfare -= instance.welfare
	member.fines -= instance.fines
	member.other -= instance.other
	member.save()


def tulinaaweContributor_post_save(sender, instance, **kwargs):
	contributor = instance
	event = contributor.event
	event.total_amount_contributed += contributor.amount
	event.save()


def loan_payment_post_save(sender, instance, **kwargs):
	loan = instance.loan
	loan.amount_paid += instance.amount
	loan.save()

	if loan.amount_paid > loan.amount:
		loan.interest = loan.amount_paid - loan.amount
		loan.save()


def expense_items_post_save(sender, instance, **kwargs):
	expense = instance.expense
	expense.items_no += 1
	expense.total_amount += instance.total_value
	expense.save()


def expense_items_pre_delete(sender, instance, **kwargs):
	if instance.expense:
		expense = instance.expense
		expense.items_no -= 1
		expense.total_amount -= instance.total_value
		expense.save()


def tulinaaweContributor_pre_delete(sender, instance, **kwargs):
	if instance.event:
		contributor = instance
		event = instance.event
		event.total_amount_contributed -= contributor.amount
		event.save()


def loan_payment_pre_delete(sender, instance, **kwargs):
	if instance.loan:
		loan = instance.loan
		loan.amount_paid -= instance.amount
		loan.save()

		if loan.amount_paid < loan.amount:
			loan.interest = 0
			loan.save()


#Post Saves

post_save.connect(tulinaaweContributor_post_save, sender=models.TulinaaweContributor,dispatch_uid=uuid.uuid4)

post_save.connect(transaction_post_save, sender=models.Transaction, dispatch_uid=uuid.uuid4)

post_save.connect(loan_payment_post_save, sender=models.LoanPayment, dispatch_uid=uuid.uuid4)

post_save.connect(expense_items_post_save, sender=models.ExpenseItem, dispatch_uid=uuid.uuid4)


#Pre deletes

pre_delete.connect(transaction_pre_delete, sender=models.Transaction, dispatch_uid=uuid.uuid4)

pre_delete.connect(expense_items_pre_delete, sender=models.ExpenseItem, dispatch_uid=uuid.uuid4)

pre_delete.connect(loan_payment_pre_delete, sender=models.LoanPayment, dispatch_uid=uuid.uuid4)

pre_delete.connect(tulinaaweContributor_pre_delete, sender=models.TulinaaweContributor, dispatch_uid=uuid.uuid4)

