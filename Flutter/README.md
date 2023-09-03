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

- Classes, setState, "${}"

- +Widgets used: Scaffold (Base screen), Container, BoxDecoration, LinearGradient, Center, Column, TextButton
- Classes used: StatelessWidgets, StatefulWidget, Alignment, MainAxisSize, Image, EdgeInsets, Colors, TextStyle, Text
```

- [exercise_2_quiz](exercise_2_quiz): 
```
- Opacity is performance-intensive! use alpha in Color.fromARGB(150, 255, 255, 255) instead
- Alternative constructors Eg. OutlinedButton vs OutlinedButton.icon for icon
- Margin vs Padding
- Installing 3rd party packages (GoogleFonts)
- Getters: "getting a value", used as a property, internally is a method
- .shuffle() to randomly shuffle mutate in-place, List.of(...) to create copy of list, .add(), .map(), .where(), Map<keyType, valueType>, Map typecasting as Dart doesn't know type of value in Map Eg. data["qn_index"] as int

- +Widgets used: SizedBox (spacing), RoundedRectangleBorder, SizedBox + SingleChildScrollView (for scrollable window)
- Classes used: BorderRadius, CrossAxisAlignment, Icons
```

- [exercise_3_expense_tracker](exercise_3_expense_tracker): 
```
- DateTime, Category, 
- IOS vs Android Dialog Responsiveness
- Portrait vs Landscape Orientation Responsiveness
- Futures (Promises), Async Await Eg. Adding item
- Theming (.copyWith(...), .of(context) from ThemeData)
- 3rd party (uuid (unique ids), intl (date formatter))

- +Widgets used: showModalBottomSheet (Overlay), ScaffoldMessenger, SnackBar (Eg. Undo notification), AppBar (Row Toolbar at top), Chart, Expanded (use when 2 nested widgets are unconstrained by space), CupertinoAlertDialog (IOS native), AlertDialog (Android),  LayoutBuilder (constraints based on parent widget), DropdownButton, DropdownMenuItem, Navigator.push/pushReplacement/pop(context, {...}) (Add/Replace/Remove overlay (return to prev screen) & pass info along),  ListView.builder (Scrollable List, BUT only create when visible (scrolled into view) for performance), Dismissible, FractionallySizedBox
- Classes used: Enum, ColorScheme, Brightness, WidgetsFlutterBinding, SystemChrome, DeviceOrientation, ThemeData, CardTheme, ElevatedButtonThemeData, AppBarTheme, CardTheme, ThemeMode, MediaQuery, TextEditingController (manage memory storage of input field, .dispose()), Platform.is..., ValueKey, TextInputType (Keyboard type for email/numbers), MaterialPageRoute (Route into another screen)
```

- [exercise_4_meals_app](exercise_4_meals_app): 
```
- late
- Cross-widget/App-wide state
- Explicit, Implicit Animations
- 3rd party (riverpod (Manage cross-widget state instead of passing states thru widgets that don't use it))

- +Widgets used: Drawer (Hamburger icon Sidebar), BottomNavigationBar (Tab bar at bottom), BottomNavigationBarItem, Card, GestureDetector (just make tappable), InkWell(make tappable + give visual feedback), Stack(Eg. text (child) on image (parent), starting with bottom (most background) layer), Hero (Animate widget across diff screens, need to be tagged same for connection), Positioned ( how child should be positioned RELATIVE to parent on stack), ListTile (Outputting any type List as a row), SwitchListTile (Row of switches), AnimatedSwitcher, GridView (similar to ListView, but grids)
- Classes used: ProviderScope, ConsumerStatefulWidget + ConsumerState, ref.watch(PROVIDER) (read again whenever value changes, like JS hooks), ref.read(PROVIDER.notifier)... (read once), StateNotifier(.state holds data, BUT cannot modify (.add/.remove) regardless, MUST alw create new data), StateNotifierProvider, FadeInImage (Fade in instead of popping in animation), MemoryImage (Image loaded from memory), NetworkImage (Image loaded from internet), BoxFit.cover (If image is too big to fit, it is cut off and zoomed in, not distorted), TextOverflow (What to replace with if text overflows, Eg. .ellipsis), RotationTransition (transition animation), Tween, WillPopScope (Detected when user taps back button (device/app)), AnimationController (late, .forward/.stop/.repeat, .dispose(), .value), AnimatedBuilder (Listen to animation), SliverGridDelegateWithFixedCrossAxisCount (Set no. of columns for GridView), CurvedAnimation (Non-linear animation)
```

- [exercise_5_shopping_list](exercise_5_shopping_list): 
```
- Form
- Backend & HTTP requests
- json.decode/encode
- 3rd party (http.get/post/put/patch/delete(...))

- +Widgets used: CircularProgressIndicator (loading spinner), FutureBuilder (Updating UI based on state of Future)
- Classes used: Uri.https(...),
```
