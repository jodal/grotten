<h1 align="center">
   &#x1F409;<br>
   grotten
</h1>

<p align="center">
  <em>text-based dungeon explorer developed together with an 8-year-old</em>
</p>

## Disclaimer

Grotten is a very basic text-based dungeon explorer. It is probably only
entertaining to the two core developers.

## Developers

- **The dad**, who has fun modelling game state and refactoring over and over,
  while trying to teach some basics related to computers, programming, and
  Python to the iPad generation.

- **The 8-year-old son**, who is constantly wondering when we're reaching
  feature parity with _Zelda: Breath of the Wild_.

## Usage

1. Clone Git repo and change into the project directory:

   ```
   git clone git@github.com:jodal/grotten.git
   cd grotten
   ```

2. Install dependencies with [uv](https://docs.astral.sh/uv/):

   ```
   uv sync
   ```

3. List available command line options:

   ```
   uv run grotten --help
   ```

4. Run the game:

   ```
   uv run grotten play
   ```

## Translations

Translations is somewhat supported through gettext. Specify the `LANG`
environment variable to change translation. E.g. to change language to
Norwegian Bokmål:

    LANG=nb uv run grotten
