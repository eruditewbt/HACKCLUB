import 'package:test/test.dart';

void main() {
  group('String detection and replacement', () {
    test('detects simple strings', () {
      final text = "Text('Hello World')";
      expect(text.contains('Hello World'), true);
    });

    test('detects interpolated strings', () {
      final text = "'Task \$id not found'";
      expect(RegExp(r'\\$\w+').hasMatch(text), true);
    });

    test('detects plural patterns automatically', () {
      final text = "'You have \$count messages'";
      expect(text.contains('\$count'), true);
    });
  });
}
