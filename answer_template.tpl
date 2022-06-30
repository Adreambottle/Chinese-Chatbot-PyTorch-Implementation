<html>
    <head>
    <title>my answer</title>
    </head>
    <body>
    <h1>Answer Page</h1>
    <p>
    %if Question:
        <p>您的问题是：{{ Question }}</p>
        <p>问题经过分词后是：{{ question_token }}</p>
        <p>您可能是想问：{{ output_question }}</p>
        <p>问题的答案是：{{ output_answer }}</p>

    %else:
        <i>好像没有问题</i>
    %end
    </p>
    </body>
</html>