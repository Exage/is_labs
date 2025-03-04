% ===================== ФАКТЫ СЕМАНТИЧЕСКОЙ СЕТИ =====================
% Предметная область: Университет

% 1. Возрастные группы студентов
age(alice, under18).
age(bob, between18and30).
age(charlie, over30).
age(dave, between18and30).

% 2. Предпочтения (специализации) студентов
preference(alice, math).
preference(bob, cs).
preference(charlie, physics).
preference(dave, cs).

% 3. Рекомендуемые курсы для каждой специализации
recommends(math, linearAlgebra).
recommends(cs, algorithms).
recommends(physics, quantumMechanics).

% 4. Преподаватели курсов
teacher(linearAlgebra, assocProfBrown).
teacher(algorithms, profJohnson).
teacher(quantumMechanics, drIvanov).

% 5. Студенты, посещающие курсы
attends(alice, linearAlgebra).
attends(bob, algorithms).
attends(charlie, quantumMechanics).
attends(dave, algorithms).

% 6. Руководители (адвайзеры) студентов
advisor(assocProfBrown, alice).
advisor(profJohnson, bob).
advisor(drIvanov, charlie).
advisor(profJohnson, dave).

% 7. Принадлежность курсов к факультетам
belongsTo(linearAlgebra, faculty_science).
belongsTo(algorithms, faculty_engineering).
belongsTo(quantumMechanics, faculty_science).

% 8. Университет и его факультеты
university(uni_xyz).
faculty(faculty_science).
faculty(faculty_engineering).

partOf(faculty_science, uni_xyz).
partOf(faculty_engineering, uni_xyz).

% 9. Преподаватели и факультеты, где они работают
worksAt(assocProfBrown, faculty_science).
worksAt(profJohnson, faculty_engineering).
worksAt(drIvanov, faculty_science).

% ===================== КОММЕНТАРИИ К ЗАПРОСАМ =====================
%
% Примеры запросов:
%
% 1. Какой возрастной группе принадлежит Alice?
%    ?- age(alice, X).
%
% 2. Кто из студентов предпочитает специализацию cs?
%    ?- preference(Student, cs).
%
% 3. Какой курс рекомендует специализация math?
%    ?- recommends(math, Course).
%
% 4. Кто является преподавателем курса algorithms?
%    ?- teacher(algorithms, Teacher).
%
% 5. Какие студенты посещают курс algorithms?
%    ?- attends(Student, algorithms).
%
% 6. Кто является адвайзером студента bob?
%    ?- advisor(Teacher, bob).
%
% 7. Какому факультету принадлежит курс linearAlgebra?
%    ?- belongsTo(linearAlgebra, Faculty).
%
% 8. Какие факультеты являются частью университета uni_xyz?
%    ?- partOf(Faculty, uni_xyz).
%
% 9. Какие преподаватели работают на факультете faculty_science?
%    ?- worksAt(Teacher, faculty_science).
%
% 10. Найти цепочку «Студент → Специализация → Рекомендуемый курс → Преподаватель».
%     ?- preference(Student, Spec), recommends(Spec, Course), teacher(Course, Teacher).
%
% ===================== КОНЕЦ ФАЙЛА =====================
