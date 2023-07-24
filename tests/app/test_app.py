from src.app.main import read_root


class Test_App:
    def test_read_root(self):
        resp = read_root()

        assert resp == {
            "apiversion": "1",
            "author": "alexZ7000",
            "color": "#888888",
            "head": "scarf",
            "tail": "coffee",
            "version": "0.0.1-beta"
        }
