import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 1380, 760
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multi-Algorithm Sorting Visualization")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_GRAY = (220, 220, 220)

# Fonts
FONT = pygame.font.Font(None, 22)
TITLE_FONT = pygame.font.Font(None, 24)

# Constants
INFO_HEIGHT = 60
PADDING = 10

# Sorting algorithms
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            yield arr, j, j+1, False  # Comparing
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield arr, j, j+1, True  # Swapping
    yield arr, -1, -1, True  # Sorting complete

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            yield arr, min_idx, j, False  # Comparing
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        yield arr, i, min_idx, True  # Swapping
    yield arr, -1, -1, True  # Sorting complete

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            yield arr, j, j+1, False  # Comparing
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        yield arr, j+1, i, True  # Inserting
    yield arr, -1, -1, True  # Sorting complete

def merge_sort(arr):
    def merge(arr, l, m, r):
        left = arr[l:m+1]
        right = arr[m+1:r+1]
        i = j = 0
        k = l
        while i < len(left) and j < len(right):
            yield arr, k, m+1+j, False  # Comparing
            if left[i] <= right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
            yield arr, k-1, -1, True  # Placing
        
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
            yield arr, k-1, -1, True  # Placing
        
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
            yield arr, k-1, -1, True  # Placing

    def mergesort(arr, l, r):
        if l < r:
            m = (l + r) // 2
            yield from mergesort(arr, l, m)
            yield from mergesort(arr, m + 1, r)
            yield from merge(arr, l, m, r)

    yield from mergesort(arr, 0, len(arr) - 1)
    yield arr, -1, -1, True  # Sorting complete

class SortVisualization:
    def __init__(self, algorithm, name, position):
        self.algorithm = algorithm
        self.name = name
        self.position = position
        self.array = self.generate_array()
        self.sorting = False
        self.generator = None
        self.start_time = 0
        self.elapsed_time = 0
        self.compare_indices = (-1, -1)
        self.swap_index = -1
        self.completed = False

    def generate_array(self):
        return [random.randint(1, 100) for _ in range(50)]

    def start_sort(self):
        self.sorting = True
        self.completed = False
        self.generator = self.algorithm(self.array.copy())
        self.start_time = time.time()

    def update(self):
        if self.sorting and not self.completed:
            try:
                self.array, i, j, swapped = next(self.generator)
                self.elapsed_time = time.time() - self.start_time
                if i == -1 and j == -1:
                    self.completed = True
                else:
                    self.compare_indices = (i, j)
                    self.swap_index = i if swapped else -1
            except StopIteration:
                self.sorting = False
                self.completed = True

    def draw(self, surface, maximized=False):
        if maximized:
            rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        else:
            rect = pygame.Rect(self.position[0] * WIDTH // 2, self.position[1] * HEIGHT // 2,
                               WIDTH // 2, HEIGHT // 2)
        
        pygame.draw.rect(surface, WHITE, rect)
        pygame.draw.rect(surface, BLACK, rect, 2)

        # Info area
        info_rect = pygame.Rect(rect.x, rect.y, rect.width, INFO_HEIGHT)
        pygame.draw.rect(surface, LIGHT_GRAY, info_rect)

        title = TITLE_FONT.render(self.name, True, BLACK)
        surface.blit(title, (rect.x + PADDING, rect.y + PADDING))

        time_text = FONT.render(f"Time: {self.elapsed_time:.2f}s", True, BLACK)
        surface.blit(time_text, (rect.x + PADDING, rect.y + INFO_HEIGHT - FONT.get_height() - PADDING))

        # Bars area
        bars_rect = pygame.Rect(rect.x, rect.y + INFO_HEIGHT, rect.width, rect.height - INFO_HEIGHT)
        bar_width = bars_rect.width // len(self.array)
        for i, height in enumerate(self.array):
            if self.completed:
                color = GREEN
            elif i in self.compare_indices:
                color = RED
            elif i == self.swap_index:
                color = RED
            elif self.sorting:
                color = BLUE
            else:
                color = BLUE
            
            pygame.draw.rect(surface, color,
                             (bars_rect.x + i * bar_width, 
                              bars_rect.bottom - height * bars_rect.height // 100,
                              bar_width - 1, height * bars_rect.height // 100))

def main():
    sorts = [
        SortVisualization(bubble_sort, "Bubble Sort : Sorting of List len (50)  Range (10 -100)", (0, 0)),

        SortVisualization(selection_sort, "Selection Sort : Sorting of List len (50) Range (10 -100)", (1, 0)),
        SortVisualization(insertion_sort, "Insertion Sort : Sorting of List len (50) Range (10 -100)", (0, 1)),
        SortVisualization(merge_sort, "Merge Sort : Sorting of List len (50) Range (10 -100)", (1, 1))
    ]

    maximized = None
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if maximized is None:
                    for i, sort in enumerate(sorts):
                        if sort.position == (event.pos[0] // (WIDTH // 2), event.pos[1] // (HEIGHT // 2)):
                            maximized = i
                            break
                else:
                    maximized = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for sort in sorts:
                        if not sort.sorting:
                            sort.start_sort()
                elif event.key == pygame.K_r:
                    for sort in sorts:
                        sort.array = sort.generate_array()
                        sort.sorting = False
                        sort.completed = False
                        sort.elapsed_time = 0

        screen.fill(WHITE)

        if maximized is not None:
            sorts[maximized].update()
            sorts[maximized].draw(screen, maximized=True)
        else:
            for sort in sorts:
                sort.update()
                sort.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()