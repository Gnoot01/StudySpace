[Flutter & Dart - The Complete Guide [2023 Edition]](https://nlbsg.udemy.com/course/learn-flutter-dart-to-build-ios-android-apps/)

- [exercise_1_dice_roll](exercise_1_dice_roll): 
```
- Flutter is UI Framework for cross-platform (Android, IOS, Web, Windows, macOS, Linux) powered by Dart language, natively compiled. However, need macOS for IOS + macOS, for Appstore. Windows for Android + Web
- Flutter creates UI by nesting widgets (widget tree), inside runApp(), inside main(), which gets executed automatically by Dart
- varName, functionName, ClassName, file_name.dart conventions

- const is immutable compile-time constant
- final is mutable run-time constant
- var

- Primitive Object, Bool, String, num, int, double
- Complex Widgets

- WidgetType widget1(positionalParameter, [b], [c = 5]) {...}
- WidgetType widget1({ namedParameter1, namedParameter2 = 5 }) {...}
- WidgetType widget1(a, {required b}) {...}

- Classes, StatelessWidgets, StatefulWidget, setState, "${}"

- +Widgets used: Scaffold, Container, BoxDecoration, LinearGradient, Center, Column, TextButton
- Classes used: Alignment, MainAxisSize, Image, EdgeInsets, Colors, TextStyle, Text
```

- [exercise_2_quiz](exercise_2_quiz): 
```
- Opacity is performance-intensive! use alpha in Color.fromARGB(150, 255, 255, 255) instead
- Alternative constructors Eg. OutlinedButton vs OutlinedButton.icon for icon
- Margin vs Padding
- Installing 3rd party packages (GoogleFonts)
- Getters: "getting a value", used as a property, internally is a method
- .shuffle() to randomly shuffle mutate in-place, List.of(...) to create copy of list, .add(), .map(), .where(), Map<keyType, valueType>, Map typecasting as Dart doesn't know type of value in Map Eg. data["qn_index"] as int

- +Widgets used: SizedBox, RoundedRectangleBorder, SizedBox + SingleChildScrollView for scrollable window
- Classes used: BorderRadius, CrossAxisAlignment, Icons
```
