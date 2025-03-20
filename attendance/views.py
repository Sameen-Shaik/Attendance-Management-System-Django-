from uuid import uuid4
from django.shortcuts import render, redirect, get_object_or_404
from  .models import CourseBatch, Course,Attendance, Session
from django.db.models import Count, Q
from authenticate.models import Faculty, Student
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta
from collections import defaultdict
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def student_dashboard(request):
    user = request.user
    student = Student.objects.get(user=user)
    classes_data = []
    overall_attended = 0
    overall_total = 0

    if student:    
        courses = CourseBatch.objects.filter(students=student).select_related('course')
        
        for course in courses:
            # Get all sessions for this course
            sessions = Session.objects.filter(course_batch=course)
            total_sessions = sessions.count()
            
            # Get attendance records for this student in this course
            attended_sessions = Attendance.objects.filter(
                session__course_batch=course,
                student=student,
                status='present'
            ).count()
            
            # Calculate attendance percentage
            attendance_percentage = (attended_sessions / total_sessions * 100) if total_sessions > 0 else 0
            
            # Update overall counts
            overall_attended += attended_sessions
            overall_total += total_sessions
            
            # Add course data with attendance information
            classes_data.append({
                'course': course,
                'total_sessions': total_sessions,
                'attendance_percentage': round(attendance_percentage, 1)
            })
    
    # Calculate overall attendance percentage
    overall_percentage = (overall_attended / overall_total * 100) if overall_total > 0 else 0
    
    context = {
        'user': user,
        'classes': classes_data,
        'overall_percentage': round(overall_percentage, 1),
        'classes_attended': overall_attended
    }

    return render(request, 'attendance/student_dashboard.html', context)
    
def faculty_dashboard(request):
    user=request.user
    
    faculty = Faculty.objects.get(user=user) 

    if faculty:
        classes = CourseBatch.objects.filter(faculty=faculty).annotate(
            num_of_students=Count('students')
        )
    else:
        classes = []
    context = {
        'user': user,
        'classes': classes,
    }

    return render(request, 'attendance/faculty_dashboard.html', context)



def take_attendance(request, session_id=None):
    user = request.user
    faculty = get_object_or_404(Faculty, user=user)
    classes = CourseBatch.objects.filter(faculty=faculty)

    selected_course = None
    students = []
    session = None

    if request.method == 'POST':
        selected_course_id = request.POST.get('course_id')

        if selected_course_id:
            selected_course = get_object_or_404(CourseBatch, id=selected_course_id)
            students = selected_course.students.all()

            session = Session.objects.create(course_batch=selected_course, session_id=uuid4())
            session_id = session.session_id  

            return redirect('take_attendance_with_session', session_id=session_id)  

        if session_id and 'attendance_submit' in request.POST:
            session = get_object_or_404(Session, session_id=session_id)
            selected_course = session.course_batch
            students = selected_course.students.all()

            for student in students:
                attendance_status = request.POST.get(f'attendance_{student.user.username}', 'absent')  
                
                Attendance.objects.update_or_create(
                    session=session,
                    student=student,
                    defaults={'status': attendance_status}
                )

            return redirect('faculty_dashboard') 

    if session_id:
        session = get_object_or_404(Session, session_id=session_id)
        selected_course = session.course_batch
        students = selected_course.students.all()

    context = {
        'classes': classes,
        'selected_course': selected_course,
        'students': students,
        'session_id': session_id,
    }
    return render(request, 'attendance/take_attendance.html', context)

def student_view_attendance(request):
    user = request.user
    student = Student.objects.get(user=user)
    attendance_data = []

    if student:
        courses = CourseBatch.objects.filter(students=student)
        for course in courses:
            # Get all sessions for this course
            sessions = Session.objects.filter(course_batch=course)
            total_sessions = sessions.count()
            
            # Get attendance records for this student in this course
            attended_sessions = Attendance.objects.filter(
                session__course_batch=course,
                student=student,
                status='present'
            ).count()
            
            # Calculate attendance percentage
            attendance_percentage = (attended_sessions / total_sessions * 100) if total_sessions > 0 else 0
            
            attendance_data.append({
                'course': course,
                'total_sessions': total_sessions,
                'attended_sessions': attended_sessions,
                'attendance_percentage': round(attendance_percentage, 2)
            })
    else:
        courses = []
        attendance_data = []

    context = {
        'user': user,
        'attendance_data': attendance_data
    }
    return render(request, 'attendance/student_view_attendance.html', context)

def faculty_view_attendance(request, course_batch_id=None):
    try:
        user = request.user
        faculty = get_object_or_404(Faculty, user=user)
        
        # Get all courses taught by the faculty
        courses = CourseBatch.objects.filter(faculty=faculty)
        
        selected_course = None
        attendance_data = []
        
        if course_batch_id:
            selected_course = get_object_or_404(CourseBatch, id=course_batch_id, faculty=faculty)
            students = selected_course.students.all()
            
            # Get all sessions for this course
            sessions = Session.objects.filter(course_batch=selected_course).order_by('-date')
            total_sessions = sessions.count()
            
            # Calculate attendance for each student
            for student in students:
                try:
                    attended_sessions = Attendance.objects.filter(
                        session__course_batch=selected_course,
                        student=student,
                        status='present'
                    ).count()
                    
                    attendance_percentage = (attended_sessions / total_sessions * 100) if total_sessions > 0 else 0
                    
                    # Get detailed attendance for last 5 sessions
                    recent_attendance = []
                    for session in sessions[:5]:
                        attendance = Attendance.objects.filter(
                            session=session,
                            student=student
                        ).first()
                        recent_attendance.append({
                            'date': session.date,
                            'status': attendance.status if attendance else 'N/A'
                        })
                    
                    attendance_data.append({
                        'student': student,
                        'total_sessions': total_sessions,
                        'attended_sessions': attended_sessions,
                        'attendance_percentage': round(attendance_percentage, 2),
                        'recent_attendance': recent_attendance
                    })
                except Exception as e:
                    # Log the error and continue with next student
                    print(f"Error processing attendance for student {student}: {str(e)}")
                    continue
        
        context = {
            'courses': courses,
            'selected_course': selected_course,
            'attendance_data': attendance_data
        }
        return render(request, 'attendance/faculty_view_attendance.html', context)
    
    except Exception as e:
        # Log the error and show error message
        print(f"Error in faculty_view_attendance: {str(e)}")
        context = {
            'error_message': 'An error occurred while fetching attendance data.'
        }
        return render(request, 'attendance/faculty_view_attendance.html', context)

def student_reports(request):
    user = request.user
    student = Student.objects.get(user=user)
    attendance_data = []
    daily_data = []
    daily_labels = []
    course_data = []
    course_labels = []
    course_analysis = []
    overall_percentage = 0
    total_classes = 0
    classes_attended = 0
    best_course = "N/A"
    best_attendance = 0

    if student:
        courses = CourseBatch.objects.filter(students=student)
        total_attended = 0
        total_sessions = 0

        # Get current month's date range
        today = datetime.now()
        start_date = today.replace(day=1)  # First day of current month
        if today.month == 12:
            end_date = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end_date = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
        
        # Initialize daily attendance tracking
        daily_attendance_data = defaultdict(lambda: {'total': 0, 'present': 0})

        for course in courses:
            # Get all sessions for this course
            sessions = Session.objects.filter(course_batch=course)
            total_sessions_course = sessions.count()
            
            # Get attendance records for this student in this course
            attended_sessions = Attendance.objects.filter(
                session__course_batch=course,
                student=student,
                status='present'
            ).count()
            
            # Calculate attendance percentage
            attendance_percentage = (attended_sessions / total_sessions_course * 100) if total_sessions_course > 0 else 0
            
            # Update totals
            total_attended += attended_sessions
            total_sessions += total_sessions_course

            # Track best performing course
            if attendance_percentage > best_attendance:
                best_attendance = attendance_percentage
                best_course = f"{course.course.name} ({attendance_percentage:.1f}%)"

            # Add to attendance data
            attendance_data.append({
                'course': course,
                'total_sessions': total_sessions_course,
                'attended_sessions': attended_sessions,
                'attendance_percentage': round(attendance_percentage, 1)
            })

            # Add to course analysis
            course_analysis.append({
                'name': course.course.name,
                'code': course.course.code,
                'attendance_percentage': round(attendance_percentage, 1),
                'attended': attended_sessions,
                'total': total_sessions_course
            })

            # Add to chart data
            course_labels.append(course.course.code)
            course_data.append(round(attendance_percentage, 1))

            # Get daily attendance data for current month
            daily_records = Attendance.objects.filter(
                session__course_batch=course,
                student=student,
                session__date__range=[start_date, end_date]
            ).order_by('session__date')

            # Aggregate daily attendance
            for record in daily_records:
                date_key = record.session.date
                daily_attendance_data[date_key]['total'] += 1
                if record.status == 'present':
                    daily_attendance_data[date_key]['present'] += 1

        # Generate daily labels and data
        for date in sorted(daily_attendance_data.keys()):
            daily_labels.append(date.strftime('%d %b'))  # Format: "DD Mon"
            day_data = daily_attendance_data[date]
            percentage = (day_data['present'] / day_data['total']) * 100 if day_data['total'] > 0 else 0
            daily_data.append(round(percentage, 1))

        # Calculate overall statistics
        overall_percentage = (total_attended / total_sessions * 100) if total_sessions > 0 else 0
        total_classes = total_sessions
        classes_attended = total_attended

    context = {
        'attendance_data': attendance_data,
        'daily_labels': daily_labels,
        'daily_data': daily_data,
        'course_labels': course_labels,
        'course_data': course_data,
        'course_analysis': course_analysis,
        'overall_percentage': round(overall_percentage, 1),
        'total_classes': total_classes,
        'classes_attended': classes_attended,
        'best_course': best_course,
        'date_range': {
            'start': start_date.strftime('%d %B %Y'),
            'end': end_date.strftime('%d %B %Y')
        }
    }
    
    return render(request, 'attendance/student_reports.html', context)

@login_required
def faculty_reports(request):
    try:
        faculty = request.user.faculty
        courses = CourseBatch.objects.filter(faculty=faculty)
        
        context = {
            'courses': courses
        }
        
        course_batch_id = request.GET.get('course_batch_id')
        if course_batch_id:
            selected_course = get_object_or_404(CourseBatch, id=course_batch_id, faculty=faculty)
            context['selected_course'] = selected_course
            
            # Get date range (last 6 months)
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=180)
            
            # Get all sessions and attendance for the selected course
            sessions = Session.objects.filter(
                course_batch=selected_course,
                date__range=[start_date, end_date]
            ).order_by('date')
            
            if sessions.exists():
                # Get all students in the course
                students = Student.objects.filter(courses=selected_course)
                total_students = students.count()
                
                # Calculate monthly attendance trend
                monthly_attendance = defaultdict(lambda: {'total': 0, 'present': 0})
                for session in sessions:
                    month = session.date.strftime('%Y-%m')
                    monthly_attendance[month]['total'] += 1
                    present_count = Attendance.objects.filter(
                        session=session,
                        status='present'
                    ).count()
                    monthly_attendance[month]['present'] += present_count
                
                # Prepare monthly data for chart
                months = sorted(monthly_attendance.keys())
                monthly_labels = [datetime.strptime(m, '%Y-%m').strftime('%b %Y') for m in months]
                monthly_data = [
                    round((monthly_attendance[m]['present'] / monthly_attendance[m]['total']) * 100, 1)
                    if monthly_attendance[m]['total'] > 0 else 0
                    for m in months
                ]
                
                # Calculate student-wise attendance
                total_sessions = sessions.count()
                student_data = []
                performance_ranges = [0, 0, 0, 0]  # 0-25%, 26-50%, 51-75%, 76-100%
                students_above_threshold = 0
                total_attendance = 0
                
                for student in students:
                    attended_sessions = Attendance.objects.filter(
                        session__in=sessions,
                        student=student,
                        status='present'
                    ).count()
                    
                    attendance_percentage = (attended_sessions / total_sessions * 100) if total_sessions > 0 else 0
                    total_attendance += attendance_percentage
                    
                    # Update performance ranges
                    if attendance_percentage <= 25:
                        performance_ranges[0] += 1
                    elif attendance_percentage <= 50:
                        performance_ranges[1] += 1
                    elif attendance_percentage <= 75:
                        performance_ranges[2] += 1
                    else:
                        performance_ranges[3] += 1
                        students_above_threshold += 1
                    
                    student_data.append({
                        'name': student.user.get_full_name(),
                        'roll_number': student.roll_number,
                        'attended': attended_sessions,
                        'total': total_sessions,
                        'attendance_percentage': round(attendance_percentage, 1)
                    })
                
                # Sort student data by attendance percentage (descending)
                student_data.sort(key=lambda x: x['attendance_percentage'], reverse=True)
                
                # Calculate average attendance
                average_attendance = round(total_attendance / total_students, 1) if total_students > 0 else 0
                
                context.update({
                    'attendance_data': True,
                    'start_date': start_date,
                    'end_date': end_date,
                    'monthly_labels': monthly_labels,
                    'monthly_data': monthly_data,
                    'student_data': student_data,
                    'total_sessions': total_sessions,
                    'total_students': total_students,
                    'students_above_threshold': students_above_threshold,
                    'average_attendance': average_attendance,
                    'performance_ranges': performance_ranges
                })
            else:
                context['attendance_data'] = False
        
        return render(request, 'attendance/faculty_reports.html', context)
        
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return render(request, 'attendance/faculty_reports.html', {'error_message': str(e)})