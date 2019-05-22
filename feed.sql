
DROP TABLE IF EXISTS question;
DROP TABLE IF EXISTS tag;

CREATE TABLE question (
  id SERIAL PRIMARY KEY, 
  author int DEFAULT NULL,
  title varchar(255) DEFAULT NULL,
  content varchar(255) DEFAULT NULL,
  tags int DEFAULT NULL,
);


CREATE TABLE tag (
  id SERIAL PRIMARY KEY,
  content varchar(255) DEFAULT NULL,
  color_code varchar(255) DEFAULT NULL
);

--INSERT
INSERT INTO tag (id, content, color_code)
  VALUES ( 1, 'HTML', '#FF4000'),
  VALUES ( 2, 'CSS', '#2E9AFE'), 
  VALUES ( 3, 'JS', '#FFFF00');

INSERT INTO question (author, title, content, tags)
  VALUES ( 1, 'Does a hyperlink only apply to text?', '', 1),
  VALUES ( 1, 'What is semantic HTML?', '', 2),
  VALUES ( 1, 'Can you create a multi colored text on a web page?', '', [1, 2]),
  VALUES ( 1, 'What is ‘NaN’? What is its type?', '', 3),
  VALUES ( 1, 'What will be the output when the following code is executed?', 'var x = 21;\nvar girl = function () {\nconsole.log(x);\nvar x = 20;\n};\ngirl ();', 3),
  
