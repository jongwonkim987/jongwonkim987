USE testdatabase;

-- employees 테이블을 생성해주세요
/*employees
CREATE TABLE employees(
	employee_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    position VARCHAR(100),
    salary DECIMAL(10,2)
);
-- 계속 젹혀있는 상태일때 이미 생성된 테이블이라고 오류가 떠서 주석 처리*/
-- 직원 데이터를 employees에 추가해주세요
INSERT INTO employees (name, position, salary) VALUES ("혜민", "PM", 90000);
INSERT INTO employees (name, position, salary) VALUES ("은우", "Frontend", 80000);
INSERT INTO employees (name, position, salary) VALUES ("가을", "Backend", 92000);
INSERT INTO employees (name, position, salary) VALUES ("지수", "Frontend", 7800);
INSERT INTO employees (name, position, salary) VALUES ("민혁", "Frontend", 96000);
INSERT INTO employees (name, position, salary) VALUES ("하온", "Backend", 130000);

-- 모든 직원의 이름과 연봉 정보만을 조회하는 쿼리를 작성해주세요
SELECT name, salary FROM employees;
SELECT DISTINCT name, salary FROM employees WHERE position = "Frontend" AND salary <= 90000;
-- 테이블이 반복적으로 출력되는 오류가 있어서 구글링을 통해 DISTINCT 추가
SET SQL_SAFE_UPDATES = 0;
UPDATE employees SET salary = 90000 WHERE name='혜린' AND position='PM';
UPDATE employees SET salary = salary * 1.10 WHERE name='혜린' AND position='PM';
SELECT employee_id, name, position, salary FROM employees WHERE name='혜린';
-- 혜민이의 salary가 제가 실행할 때마다 10%씩 올라가서 값이 계속 올라갔었습니다. 그래서 값을 90000으로 고정시키고 10% 상승시켰습니다.
UPDATE employees SET salary = salary * 1.05 WHERE position= "Backend";
DELETE FROM employees WHERE name = "민혁";
SELECT position, AVG(salary) AS average_salary FROM employees GROUP BY position;
DROP TABLE employees;