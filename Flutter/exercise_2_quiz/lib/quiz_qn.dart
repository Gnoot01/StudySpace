class QuizQn {
  const QuizQn(this.text, this.answers);

  final String text;
  final List<String> answers;

  List<String> get shuffledAns {
    // creates a copy of a list
    final shuffledList = List.of(answers);
    // .shuffle() mutates list in-place
    shuffledList.shuffle();
    return shuffledList;
  }
}
